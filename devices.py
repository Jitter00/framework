from ncclient import manager
from netmiko import ConnectHandler


class Device():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def connect(self):
        self.conn = manager.connect(
            host=self.host,
            username=self.username,
            password=self.password,
            timeout=60,
            device_params={"name": "junos"},
            hostkey_verify=False
        )

    def get_parsed_info(self, rpc, xpath=None):
        if xpath:
            return self.conn.rpc(rpc).xpath(xpath)
        return self.conn.rpc(rpc)

    def apply_config_template(self, cfg, from_file=False):
        config = open(f"configs/{cfg}").read()
        self.conn.lock()
        self.conn.load_configuration(config=config, action="set")
        diff = self.conn.compare_configuration()
        self.conn.commit()
        self.conn.unlock()
        return diff.data_xml


class LegacyDevice(Device):
    def connect(self):
        self.conn = ConnectHandler(
            device_type="juniper_junos",
            ip=self.host,
            username=self.username,
            password=self.password
        )

    def run_command(self, cmd):
        output = self.conn.send_command(cmd)
        return output

    def apply_config_template(self, cfg, from_file=False):
        result = self.conn.send_config_from_file(f"configs/{cfg}")
        self.conn.commit()
        return result

