import subprocess
import time
import os

def install(package):
  try: 
    print('Checking for package...')
    __import__(package)
  except:
    print('Package not found\nStarting install...')
    try: subprocess.check_call(['pip', 'install', package])
    except Exception as err: print(str(err)+'\nCould not install package')
    time.sleep(3)
    subprocess.check_call(['clear'])
  else:
     print(package + ' was already installed')
     time.sleep(3)
     subprocess.check_call(['clear'])

def cmd(command):
  try:
    cmd=command.split()
    subprocess.check_call(cmd)
  except Exception as err: return err

def clear(secs=0):
  time.sleep(secs)
  subprocess.check_call('clear')

def check_install(package):
  try: __import__(package)
  except: return False
  else: return True