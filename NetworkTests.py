import re
from device import Device


devices = [{"host": "vsrx1"}, {"host": "vsrx2", "legacy": "True"}]


class NetworkTests:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def connect_to_all_devices(self):
        self.dev_pool = []
        for dev in devices:
            new_dev = Device(**dev)
            new_dev.connect()
            self.dev_pool.append(new_dev)

    def disconnect_from_all_devices(self):
        for dev in self.dev_pool:
            dev.disconnect()

    def apply_initial_config(self):
        for dev in self.dev_pool:
            cfg = f"{dev.host}_initial"
            dev.apply_config(cfg)

    def apply_problem_state(self):
        problem_device = [d for d in self.dev_pool if d.host == "vsrx2"][0]
        cfg = "wrong_key"
        problem_device.apply_config(cfg)

    def apply_final_config(self):
        for dev in self.dev_pool:
            cfg = f"{dev.host}_final"
            dev.apply_config(cfg)

    def check_bgp_state(self):
        for dev in self.dev_pool:
            if dev.legacy:
                state = dev.run_command("show bgp neighbor")
                pattern = re.compile("State: .*  ")
                result = pattern.findall(state)[0]
                result = result.split(":")[1].strip()
            else:
                state = dev.run_command(
                    "<get-bgp-neighbor-information></get-bgp-neighbor-information>",
                    "//peer-state"
                )
                result = state[0].text
            if result != "Established":
                return False
        return True
