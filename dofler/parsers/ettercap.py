from base import BaseParser, log 
import re

class Parser(BaseParser):
    '''
    Ettercap password parser.  This parser interprets the output from ettercap
    (basically looking for account info) and then passes it on to the API.
    '''
    name = 'ettercap'
    ruser = re.compile(r'USER: (.*?)  ')    # USER Regex: Pulls out USER field.
    rpass = re.compile(r'PASS: (.*?)  ')    # PASS Regex: Pulls out PASS field.
    rinfo = re.compile(r'INFO: (.*?)$')     # INFO Regex: Pulls out INFO field.
    rproto = re.compile(r'^(\w*) : ')       # PROTO Regex: Pulls the protocal.

    def parse(self, line):
        '''Ettercap line output parser.'''
        if 'USER' in line:
            usernames = self.ruser.findall(line)
            passwords = self.rpass.findall(line)
            infos = self.rinfo.findall(line)
            protos = self.rproto.findall(line)
            if len(usernames) > 0 and len(passwords) > 0:
                username = usernames[0]
                password = passwords[0]
                info = infos[0]
                proto = protos[0]
                log.debug('ETTERCAP: sending Account <%s>' % username)
                self.api.account(username, password, info, proto, 'ettercap')