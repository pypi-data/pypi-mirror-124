import os


def set_debug(a):

     if a:
      os.environ['ELBA_DEBUG'] = '1'
     else: 
      os.environ['ELBA_DEBUG'] = '0'

def set_bypass(a):

     if a:
      os.environ['BYPASS_EFUNX'] = '1'
     else: 
      os.environ['BYPASS_EFUNX'] = '0'

def set_autodiff(a):

     if a:
      os.environ['ELBA_AUTODIFF'] = '1'
     else: 
      os.environ['ELBA_AUTODIFF'] = '0'

def set_compute_anyway(a):

      os.environ['ELBA_COMPUTE_ANYWAY'] = a

