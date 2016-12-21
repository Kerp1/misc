#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division  # python2 compatibility
import time
import os
import subprocess

ICONS = [("wlan1.xbm", -90),
         ("wlan2.xbm", -80),
         ("wlan3.xbm", -70),
         ("wlan3.xbm", -60),
         ("wlan4.xbm", -50),
         ("wlan5.xbm", 0)]


class Py3status:
    # Available configuration parameters
    cache_timeout = 30
    interface = "wlp58s0"
    template = "{}"

    @staticmethod    
    def get_icon(signal_strength):
        icon_name = next(icon_name for (icon_name, threshold) in ICONS if signal_strength < threshold)
        return os.path.dirname(os.path.abspath(__file__)) + "/icons/" + icon_name

    @staticmethod
    def get_signal_strength(rows):
        return int(rows[5].split(' ')[1])

    @staticmethod
    def get_ssid(rows):
        return rows[1].split(' ')[1]

    def wifi_status(self, i3_output_list, i3_config):
        response = {}
        command_output = subprocess.check_output(["iw", "dev", self.interface, "link"],
                                                  stderr=subprocess.STDOUT).decode("UTF-8")

        if command_output.startswith("Not connected"):
            response['full_text'] = self.template.format("No connection")
        else:
            rows = command_output.split('\n')

            ssid = self.get_ssid(rows)
            signal_strength = self.get_signal_strength(rows)

            icon_path = self.get_icon(signal_strength)

            response['icon'] = icon_path
            response['full_text'] = self.template.format(ssid)
            response['cached_until'] = time.time() + self.cache_timeout

        return response

if __name__ == "__main__":
    import time
    module = Py3status()
    while True:
        print(module.wifi_status([], []))
        time.sleep(1)
