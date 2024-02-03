from riocore.plugins import PluginBase


class Plugin(PluginBase):
    def setup(self):
        self.NAME = "max7219"
        self.VERILOGS = ["max7219.v"]
        self.PINDEFAULTS = {
            "mosi": {
                "direction": "output",
                "invert": False,
                "pullup": False,
            },
            "sclk": {
                "direction": "output",
                "invert": False,
                "pullup": False,
            },
            "sel": {
                "direction": "output",
                "invert": False,
                "pullup": False,
            },
        }
        self.INTERFACE = {
            "value": {
                "size": 24,
                "direction": "output",
            },
        }
        self.SIGNALS = {
            "value": {
                "min": -999999,
                "max": 999999,
                "direction": "output",
            },
        }
        self.OPTIONS = {
            "brightness": {
                "min": 0,
                "max": 15,
                "default": 15,
                "type": int,
            },
            "frequency": {
                "min": 100000,
                "max": 10000000,
                "default": 1000000,
                "type": int,
            },
        }
        self.INFO = "7segment display based on max7219"
        self.DESCRIPTION = ""

    def gateware_instances(self):
        instances = self.gateware_instances_base()
        instance = instances[self.instances_name]
        instance_predefines = instance["predefines"]
        instance_parameter = instance["parameter"]
        instance_arguments = instance["arguments"]
        brightness = self.plugin_setup.get("brightness", self.OPTIONS["brightness"]["default"])
        instance_parameter["BRIGHTNESS"] = f"8'h0{brightness:x}"
        frequency = int(self.plugin_setup.get("frequency", self.OPTIONS["frequency"]["default"]))
        divider = self.system_setup["speed"] // frequency // 5
        instance_parameter["DIVIDER"] = divider
        return instances
