from ncclient import manager
from netmiko import ConnectHandler
from robot.api.deco import keyword, library


class Device():

    def __init__(self, host, username="cristian", password="Juniper", legacy=False):
        self.host = host
        self.username = username
        self.password = password
        self.legacy = legacy

    def connect(self):
        if self.legacy:
            self.conn = ConnectHandler(
                device_type="juniper_junos",
                ip=self.host,
                username=self.username,
                password=self.password
            )
        else:
            self.conn = manager.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                timeout=60,
                device_params={"name": "junos"},
                hostkey_verify=False
            )

    def disconnect(self):
        if self.legacy:
            self.conn.disconnect()

    def run_command(self, cmd, xpath=None):
        if self.legacy:
            output = self.conn.send_command(cmd)
            return output
        else:
            if xpath:
                return self.conn.rpc(cmd).xpath(xpath)
            return self.conn.rpc(cmd)

    def apply_config(self, cfg, from_file=True):
        if self.legacy:
            if from_file:
                result = self.conn.send_config_from_file(f"configs/{cfg}")
            else:
                result = self.conn.send_config_set(cfg)
            self.conn.commit()
            self.conn.exit_config_mode()
            return result
        else:
            if from_file:
                config = open(f"configs/{cfg}").read()
            else:
                config = cfg
            self.conn.lock()
            self.conn.load_configuration(config=config, action="set")
            diff = self.conn.compare_configuration()
            self.conn.commit()
            self.conn.unlock()
            return diff.data_xml
