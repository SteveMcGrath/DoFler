from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dofler.models import *
from dofler.config import config


engine = create_engine(config.get('Database', 'path'))
Session = sessionmaker(bind=engine)


def initialize():
    Account.metadata.create_all(engine)
    Image.metadata.create_all(engine)
    Protocol.metadata.create_all(engine)
    Stat.metadata.create_all(engine)
    User.metadata.create_all(engine)
    Setting.metadata.create_all(engine)
    s = Session()
    if s.query(User).count() == 0:
        s.add(User('admin', '5f4dcc3b5aa765d61d8327deb882cf99'))
        s.add(Setting('log_console', '1'))
        s.add(Setting('log_console_level', 'info'))
        s.add(Setting('log_file', '0'))
        s.add(Setting('log_file_level', 'info'))
        s.add(Setting('log_file_path', '/var/log/dofler.log'))
        s.add(Setting('api_debug', '0'))
        s.add(Setting('api_port', '8080'))
        s.add(Setting('api_host', '127.0.0.1'))
        s.add(Setting('api_ssl', '0'))
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
        s.add(Setting('autostart', '0'))
        s.add(Setting('ettercap_enabled', '1'))
        s.add(Setting('ettercap_command', 'ettercap -Tzuqi {IF}'))
        s.add(Setting('driftnet_enabled', '1'))
        s.add(Setting('driftnet_command', 'driftnet -ai {IF} -d /tmp'))
        s.add(Setting('tshark_enabled', '1'))
        s.add(Setting('tshark_command', 'tshark -i {IF}'))


initialize()