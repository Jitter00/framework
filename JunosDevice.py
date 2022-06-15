import re
from ncclient import manager
from netmiko import ConnectHandler
from robot.api.deco import keyword, library


@library
class JunosDevice():

    @keyword
    def connect_device(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        if self.host == "vsrx2":
            self.legacy = True
        else:
            self.legacy = False
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

    def run_command(self, cmd, xpath=None):
        if self.legacy:
            output = self.conn.send_command(cmd)
            return output
        else:
            if xpath:
                return self.conn.rpc(cmd).xpath(xpath)
            return self.conn.rpc(cmd)

    @keyword
    def apply_config(self, cfg, from_file=False):
        if self.legacy:
            if from_file:
                result = self.conn.send_config_from_file(f"configs/{cfg}")
            else:
                result = self.conn.send_config_set(cfg)
            self.conn.commit()
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

    @keyword
    def check_bgp_state(self):
        if self.legacy:
            state = self.run_command("show bgp neighbor")
            pattern = re.compile("State: .*  ")
            result = pattern.findall(state)[0]
            result = result.split(":")[1].strip()
        else:
            state = self.run_command(
                "<get-bgp-neighbor-information></get-bgp-neighbor-information>",
                "//peer-state"
            )
            result = state[0].text
        return result



















