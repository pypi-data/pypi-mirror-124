import jax
import jax.numpy as jnp
import numpy as np
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import functools
import os
import time
import inspect
import shelve
from deepdiff import DeepDiff,DeepHash
#import cloudpickle as dill
import marshal as dill
import networkx as nx
import matplotlib.pylab as plt
import jaxlib
from orderedset import OrderedSet

from .__main__ import get_info as get_info,init_function

from .autodiff import *
from .utils import *
from mpi4py import MPI
import paramiko
import os
import pickle5
comm = MPI.COMM_WORLD



def run_remote(func,runner,*args):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        privatekeyfile = os.path.expanduser(runner['password'])
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        ssh.connect(runner['ip'], username = runner['username'],pkey=mykey)
       

        code = r'''import shelve
import time
with shelve.open('_client', 'c',writeback=True) as shelf:
     inputs = shelf['inputs']
     f = shelf['function']
     exec(f)
     shelf['outputs'] = list(locals().values())[-1](*inputs)
     '''

        #Create input file
        cache = os.getcwd() 
        with shelve.open(cache + '/.elba/_client', 'c',writeback=True) as shelf:
             shelf['function'] = '\n'.join(inspect.getsource(func).split('\n')[1:])
             #dill.dumps(func,protocol=3)
             shelf['inputs']   = args
             shelf['code']   = code

        #cache = os.getcwd() 
        #with shelve.open(cache + '/.elba/_client', 'r') as shelf:
        #     f = dill.loads(shelf['function'])

        #----
        sftp = ssh.open_sftp()
        sftp.put(cache+'/.elba/_client.dir', '_client.dir')
        sftp.put(cache+'/.elba/_client.bak', '_client.bak')
        sftp.put(cache+'/.elba/_client.dat', '_client.dat')
        sftp.close()

        #Execute Command
        stdin, stdout,stderr = ssh.exec_command('python3 -c "' + code + '"' )
        channel = stdout.channel
        channel.set_combine_stderr(True)
        while True:
             line = stdout.readline()
             if not line:
              break
             print(line, end="")
        #------------------

        sftp = ssh.open_sftp()
        sftp.get('_client.dir',cache+'/.elba/_client.dir')
        sftp.get('_client.bak',cache+'/.elba/_client.bak')
        sftp.get('_client.dat',cache+'/.elba/_client.dat')
        sftp.close()
         

        ssh.close()
     
        cache = os.getcwd() 
        with shelve.open(cache + '/.elba/_client', 'r') as shelf:
             outputs = shelf['outputs']
        return outputs     


def run(func,jacobians = [],runner={'name':'loc'}):

    #Compute the actual Jacobians to be computed via AD 
    info =  get_info(func)
    output_channels = info['output_channels']
    input_channels  = info['input_channels']

    AD_jacobians = []
    for jac in jacobians:
        if not jac in output_channels:
           AD_jacobians.append(jac)
    #--------       
    

    if len(AD_jacobians) == 0:

        #print('Function')  
        def wrapper(*args):
            args = get(args[0],channels=input_channels)
            if not type(args) == list: args = [args]
            if runner['name']=='loc':
             value = func(*args)
            else:
             value = run_remote(func,runner,*args)

            if not type(value) in (list,tuple): value = [value]
            value = {channel:{'data':value[n],'version':None}  for n,channel in enumerate(get_info(func)['output_channels'])}

            return {'__elba__':value} 

        return wrapper

    else:
      return jacobian(func,AD_jacobians)  



def compare_data(var1,var2):
         """compare hashable data for caching"""
         if hasattr(var1,'ndim'):
            if var1.ndim == 0: #in case of 0-d arrays
                  return var1 == var2
         if isinstance(var2,jaxlib.xla_extension.DeviceArray):
            var2 = np.array(var2) 
              
         return DeepHash(var1)[var1] == DeepHash(var2)[var2]



def get_version(channel,data):


    version = None
    if comm.rank == 0: 
     cache = os.getcwd() + '/.elba/'
     with shelve.open(cache + '/_data', 'c',writeback=True) as shelf:
            if not channel in shelf.keys():
                shelf[channel] = {0:data} #Init data
                version = 0
            else:
                for key,value in shelf[channel].items():
                    if compare_data(value,data):
                        version =  key #It is already stored
                        break
                if version == None:    
                 version = len(shelf[channel])   
                 shelf[channel].update({version:data}) 
    comm.Barrier()    
    return comm.bcast(version,root=0)


def save_state(func,inputs,outputs,jacobians=[]):
  
       """save the function state"""

       info = get_info(func)
       output_versions = None
       if comm.rank == 0:
        input_versions = [inputs['__elba__'][channel]['version'] for channel in info['input_channels'] ]
        input_versions.append(info['code'])

        cache = os.getcwd() + '/.elba/'

        output_versions = []
        with shelve.open(cache + '/_data', 'c',writeback=True) as shelf:
           for n,channel in enumerate(info['output_channels']+jacobians):
             output_versions.append(len(shelf.setdefault(channel,{})))
             shelf.setdefault(channel,{})[output_versions[-1]] = outputs['__elba__'][channel]['data']        


        with shelve.open(cache + '/_state', 'c',writeback=True) as shelf:
             shelf[info['name']].update({dill.dumps(input_versions):output_versions})
             for n,channel in enumerate(info['output_channels']):
                 print_command('SAVE ',channel + ' version ' + str(output_versions[n]))
     

       output_versions = comm.bcast(output_versions,root=0)


       for n,name in enumerate(info['output_channels']+jacobians): outputs['__elba__'][name]['version'] = output_versions[n]

       return outputs


def convert_to_elba(func,retain_state,*args):

    input_channels = get_info(func)['input_channels']

    def is_elba(x):
      if type(x) == dict:
        if '__elba__' in x.keys():
            return True
      return False  

    output = {}

    for n,arg in enumerate(args):
        if is_elba(arg):
            if retain_state:
             output.update(arg['__elba__'])
            else: 
             item = arg['__elba__']   
             output.update({input_channels[n]:list(item.values())[0]})
             translate(list(item.keys())[0],input_channels[n])

        else:
            version = get_version(input_channels[n],arg)
            output.update({input_channels[n]:{'data':arg,'version':version}})

    #Default to empty dictionaries if a channel is missing           
    for channel in input_channels:
       if not channel in output.keys():
            version = get_version(channel,{})
            print_command('Default ',channel)
            output.update({channel:{'data':{},'version':version}})

    return {'__elba__':output}

def load_state(func,inputs,jacobians=[]):


    if func.__name__ in  os.environ['ELBA_COMPUTE_ANYWAY'].split(','):
            return {'__elba__':{}}


    info = get_info(func)

    input_versions = [inputs['__elba__'][channel]['version']  for channel in info['input_channels'] ]

    for version in input_versions:
        if version == None:
            return {'__elba__':{}}

    #TODO: if the data being passed is new there is not need to check for the state. We need a flag to indicate that this is new data

    input_versions.append(info['code'])

    if comm.rank == 0:
     cache = os.getcwd() + '/.elba/'
     with shelve.open(cache + '/_state', 'r') as shelf:
           if dill.dumps(input_versions) in shelf[info['name']].keys():

               output_versions =  shelf[info['name']][dill.dumps(input_versions)]

               output = {(info['output_channels']+jacobians)[n]:{'version':version,'data':None} for n,version in enumerate(output_versions)} #There is no need to retrieve data at this point
           else: output = {}
    else: output = None

   
    output = comm.bcast(output,root=0)

    return {'__elba__':output}


def elba(_func=None, *,jacobians=[],retain_state=False,runner={'name':'loc'},filekey=None):
    def decorator(func):
        if int(os.environ['BYPASS_ELBA']) == 1:
          def wrapper(*args, **kwargs): return func(*args,**kwargs)
          return wrapper

        else:
         init_function(func)
         @functools.wraps(func)
         def wrapper(*args, **kwargs):
            args  = convert_to_elba(func,retain_state,*args)
            state = load_state(func,args,jacobians=jacobians)
            if len(state['__elba__']) == 0:
               
             print_command('RUN ',get_info(func)['name'])
             
             outputs = run(func,jacobians = jacobians,runner=runner)(args) 
             if retain_state:
              args['__elba__'].update(save_state(func,args,outputs,jacobians=jacobians)['__elba__'])
             else: 
              args = save_state(func,args,outputs,jacobians=jacobians)

            else:
             if retain_state:
              args['__elba__'].update(state['__elba__']) #for now store all the variables on the graph (gargabe will be needed)
             else: 
              args=state   

            return args

         return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

def filter_data(data,channels):

    output = {channel: data['__elba__'][channel] for channel in channels}

    return {'__elba__':output}


def load_data(channel,version=None):

    cache = os.getcwd() + '/.elba/'
    with shelve.open(cache + '/_data', 'r') as shelf:
        if version == None:
         return shelf[channel]
        else:
         return shelf[channel][version]


def load_function(function):

    cache = os.getcwd() + '/.elba/'
    with shelve.open(cache + '/_functions', 'r') as shelf:
        return dill.loads(shelf[function]['function'])
