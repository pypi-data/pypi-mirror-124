import os,shelve
import jax.numpy as jnp
import numpy as np
from termcolor import colored
from mpi4py import MPI
from flax.core.frozen_dict import FrozenDict

comm = MPI.COMM_WORLD

def print_command(cmd,text):
    if int(os.environ['ELBA_DEBUG']) == 1:
      if comm.rank == 0:    
       print(colored(cmd,'green') + text)


def get_channels():

       input_channels      = {}
       output_channels     = {}
       output_channels_map = {}
       input_channels_map = {}
       cache = os.getcwd() + '/.elba/'
       with shelve.open(cache + '/_functions', 'r') as shelf:
           for key,value in shelf.items():
               for channel in value['output_channels']:
                 output_channels[channel] = key
               for channel in value['input_channels']:
                 input_channels_map[channel] = key
               input_channels[key] = value['input_channels']
               output_channels_map[key] = value['output_channels']
  
       return input_channels,output_channels,output_channels_map,input_channels_map         


def import_pipeline(pipeline): 

      if comm.rank == 0:
       cache = os.getcwd() + '/.elba/'
       with shelve.open(cache + '/_pipelines', 'c',writeback=True) as shelf:
          path = shelf[pipeline] 
      else: path = None    
      return comm.bcast(path)


def isnan(data):

    if type(data) == np.ndarray:
        return jnp.any(jnp.isnan(data))
    else:
        return data == None



def load_variable(channel,variable):
    print_command('LOAD ',channel + ' version: ' + str(variable['version']))
    cache = os.getcwd() + '/.elba/'

    with shelve.open(cache + '/_data', 'r') as shelf:
        if not channel in shelf.keys():
           with shelve.open(cache + '/_translator', 'r') as translator:
             input_channel = channel  
             channel = translator[channel]
             print_command('TRANSLATE ',channel + ' -> ' + input_channel)
        return shelf[channel][variable['version']]


def translate(key_1,key_2):
 
     if not key_1 == key_2:
       cache = os.getcwd() + '/.elba/'
       with shelve.open(cache + '/_translator', 'c',writeback=True) as shelf:
            shelf[key_2] = key_1
     

def freeze_elba(arr):

 from flax.core.frozen_dict import freeze

 return freeze(arr)


def get(data,channels='all'):

    def get_data(value,channel):

            if isnan(value['data']):
                return load_variable(channel,value)
            else:
                return value['data']

    output = []
    if channels == 'all':
        for channel,value in data['__elba__'].items():
            output.append(get_data(value,channel))
    else:

        if not type(channels) == list: channels = [channels]
        for channel in channels:
                
            output.append(get_data(data['__elba__'][channel],channel))

    if len(output) == 1: output = output[0]

    return output
