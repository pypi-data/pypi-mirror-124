import base64
import json
import os
import sys
from bertdotbill.config import ConfigUtil
from bertdotbill.logger import Logger

logger = Logger().init_logger(__name__)

class Commands:

  def __init__(self, settings, **kwargs):
    self.settings = settings
    self.config_util = ConfigUtil()

  def retrieve(self, **kwargs):
      logger.info('Retrieving available os commands')
      commands = self.settings.get('commands', {})
      encoded = kwargs.get('encoded')

      if isinstance(commands, dict):
        commands_platform_specific = [c for c in commands.get(sys.platform, [])]
        commands_common = [c for c in commands.get('common', [])]
        osCommand_list = commands_platform_specific + commands_common
        if len(osCommand_list) > 0:
          logger.debug('OS Command List is: %s' % osCommand_list)
        else:
          logger.warning('OS Command List is empty')
          return osCommand_list
        if encoded:
          osCommands_bytes = str(json.dumps(osCommand_list)).encode("ascii")
          encoded_osCommand_list = base64.b64encode(osCommands_bytes)
          encoded_osCommands = encoded_osCommand_list.decode("utf-8")
          return encoded_osCommands
        else: 
          return osCommand_list
      else:
        logger.warning("Improperly structured 'commands' config block, seek --help")

  def launch(self, command_key, args=None):
      
      osCommands = self.retrieve()
      logger.info("Launching command mapped to '%s'" % command_key)
      cmd = None
      try:
        if isinstance(osCommands, list):
          for osCommandEntry in osCommands:
            for k,v in osCommandEntry.items():
              if k == command_key:
                cmd = v['cmd']
                logger.debug('Running command %s' % cmd)
                os.system(cmd)
          if not cmd:
            logger.warning('No command key found for %s' % command_key)
            return False
        else:
          logger.warning("Improperly structured 'commands' config block, seek --help")
      except Exception as e:
        logger.error("I had a problem reading the command to be launched, check your config and/or seek --help")
