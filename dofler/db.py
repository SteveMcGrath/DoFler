from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dofler.models import *
from dofler import config
from dofler.md5 import md5hash
import time

engine = create_engine(config.config.get('Database', 'db'), echo=False)
Session = sessionmaker(bind=engine)
setting_engine = create_engine(config.config.get('Database', 'setting_db'))
SettingSession = sessionmaker(bind=setting_engine)

def initialize():
    '''
    Database Initialization Function

    Creates all the default values for the settings databases if they are in a
    pristine state.  This is run at every startup of the code.
    '''
    Account.metadata.create_all(engine)
    Image.metadata.create_all(engine)
    Stat.metadata.create_all(engine)
    User.metadata.create_all(setting_engine)
    Setting.metadata.create_all(setting_engine)
    s = SettingSession()
    if s.query(User).count() < 1:
        s.add(User('admin', 'password'))
        s.add(Setting('log_console', '1'))
        s.add(Setting('log_console_level', 'info'))
        s.add(Setting('log_file', '0'))
        s.add(Setting('log_file_level', 'info'))
        s.add(Setting('log_file_path', '/var/log/dofler.log'))
        s.add(Setting('api_debug', '0'))
        s.add(Setting('api_port', '8080'))
        s.add(Setting('api_host', '127.0.0.1'))
        s.add(Setting('api_app_server', 'paste'))
        s.add(Setting('server_host', '127.0.0.1'))
        s.add(Setting('server_port', '8080'))
        s.add(Setting('server_ssl', '0'))
        s.add(Setting('server_anonymize', '1'))
        s.add(Setting('server_username', 'admin'))
        s.add(Setting('server_password', 'password'))
        s.add(Setting('web_images', '1'))
        s.add(Setting('web_accounts', '1'))
        s.add(Setting('web_stats', '1'))
        s.add(Setting('web_image_delay', '5'))
        s.add(Setting('web_account_delay', '30'))
        s.add(Setting('web_stat_delay', '60'))
        s.add(Setting('web_stat_max', '5'))
        s.add(Setting('web_image_max', '200'))
        s.add(Setting('web_account_max', '25'))
        s.add(Setting('web_display_settings', '1'))
        s.add(Setting('autostart', '0'))
        s.add(Setting('listen_interface', 'eth1'))
        s.add(Setting('ettercap_enabled', '1'))
        s.add(Setting('ettercap_command', 'ettercap -Tzuqi {IF}'))
        s.add(Setting('driftnet_enabled', '1'))
        s.add(Setting('driftnet_command', 'driftnet -ai {IF} -d /tmp'))
        s.add(Setting('tshark_enabled', '1'))
        s.add(Setting('flag','blood_eagle'))
        s.add(Setting('tshark_command', '/bin/bash -c \'dumpcap -i {IF} -P -w - | tshark -T psml -PS -l -r -\''))
        s.add(Setting('cookie_key', str(md5hash(time.time()))))
    s.commit()
    s.close()