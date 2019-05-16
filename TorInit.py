import re
import sys
import time
import logging
import subprocess

from stem.util import system, term
from stem import process as tor_process


class TorInit():


  def __init__(self, socks_port=9050, control_port=9051):
        
    self.socks_port = socks_port
    self.control_port = control_port
    # self.check_tor_command = "lsof -n -i :9050"
    self.check_tor_command = "lsof -i :9050"
    self.command2 = ['awk', '{print $2}']
  def _checkTorStatus(self):
    """

    if Torproxy is exist, will kill tor

    """
    proc1 = subprocess.Popen(self.check_tor_command.split(), stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(self.command2, stdin=proc1.stdout, stdout=subprocess.PIPE)
    port_status = proc2.communicate()[0]

    logging.info(port_status)
    if port_status:
      port_status = set([pid for pid in re.sub(r'\D', ' ', str(port_status)).split() if pid.isdigit()])
      logging.info(port_status)
      for pid in port_status:
        logging.info(pid)
        subprocess.Popen("kill {}".format(pid).split(), stdout=subprocess.PIPE).communicate()
        logging.info('kill tor pid {} success'.format(pid))
        
        
  

  def startTorProxy(self):
    """

    start tor and open SocksPort proxy, after _checkTorStatus function

    """
    limit_try = 0
    while True:
      try:
    
        self._checkTorStatus()

        tor_process.launch_tor_with_config(
          config={
                    'SocksPort': str(self.socks_port),
                    'ControlPort': str(self.control_port),
                  },
                  init_msg_handler=self.printBootstrapLines,
                  timeout=300
        )
        logging.info('Start tor success, socks_port : {}'.format(self.socks_port))  
        break
      except Exception as e:
        logging.info(e)
        if limit_try == 10:
          logging.info('Init tor fail.')
          break
        limit_try += 1
        logging.info('Start tor fail, limit try : {}'.format(limit_try))   
        continue

     
  def printBootstrapLines(self, line):
    if "Bootstrapped " in line:
      line = term.format(line, term.Color.GREEN)
      self.displayMsg(line)

  def displayMsg(self, msg_context, msg_type=None):
    '''
        
    Display the processing message of the process.
    
    '''
    if msg_type:
      message = '[{0}] {1} \n'.format(msg_type, msg_context)
    else:
      message = '{0} \n'.format(msg_context)
    
    sys.stdout.write(message)

