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
    error_cache_timeout = 10
    interface = "wlp58s0"
    template = "{}"
    icon_color = "#00AA00"

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

    def _create_no_connection_response(self):
        return {
            'full_text': 'No connnection',
            'cached_until': self.py3.time_in(self.error_cache_timeout),
        }

    def wifi_status(self, i3_output_list, i3_config):
        response = {}
        try:
            command_output = subprocess.check_output(["iw", "dev", self.interface, "link"],
                                                  stderr=subprocess.STDOUT).decode("UTF-8")
        except Exception as e:
            return self._create_no_connection_response()

        if command_output.startswith("Not connected"):
            return self._create_no_connection_response()
        else:
            rows = command_output.split('\n')

            ssid = self.get_ssid(rows)
            signal_strength = self.get_signal_strength(rows)

            icon_path = self.get_icon(signal_strength)

            return {
                'icon': icon_path,
                'icon_color': self.icon_color,
                'full_text': self.template.format(ssid),
                'cached_until': self.py3.time_in(self.cache_timeout),
            }

if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
