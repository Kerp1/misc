# -*- coding: utf-8 -*-
"""
Display the battery level.
Configuration parameters:
    - color_* : None means - get it from i3status config
    - format : text with "text" mode. percentage with % replaces {}
    - hide_when_full : hide any information when battery is fully charged
    - mode : for primitive-one-char bar, or "text" for text percentage ouput
Requires:
    - the 'acpi' command line
@author shadowprince, AdamBSteele
@license Eclipse Public License
"""

from __future__ import division  # python2 compatibility

import math
import subprocess

BLOCKS = ["", "", "", "", "", "", "", "", ""]
CHARGING_CHARACTER = "↑"
EMPTY_BLOCK_CHARGING = '|'
EMPTY_BLOCK_DISCHARGING = '↓'


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 30
    format = "{charging_character}{battery_block} {percent_charged}%{time_remaining}"
    notification = False

    @staticmethod
    def get_battery_block(percent_charged):
        block_index = int(math.ceil(percent_charged / 100 * (len(BLOCKS) - 1)))
        return BLOCKS[block_index]

    def __init__(self):
        self.time_remaining = ""

    def battery_level(self, i3s_output_list, i3s_config):
        #  Example acpi raw output:  "Battery 0: Discharging, 43%, 00:59:20 remaining"
        acpi_unicode = subprocess.check_output(["acpi"], stderr=subprocess.STDOUT).decode("UTF-8")

        #  Example list: ['Battery', '0:', 'Discharging', '43%', '00:59:20', 'remaining']
        acpi_list = acpi_unicode.split(' ')

        charging = True if acpi_list[2][:8] == "Charging" else False
        percent_charged = int(acpi_list[3][:-2])

        self.time_remaining = ' ' + acpi_list[4] if len(acpi_list) > 4 else ""

        format_dict = {'percent_charged': percent_charged,
                       'battery_block': self.get_battery_block(percent_charged),
                       'time_remaining': self.time_remaining,
                       'charging_character': CHARGING_CHARACTER}

        if not charging:
            format_dict['charging_character'] = ""

        full_text = self.py3.safe_format(self.format, format_dict)
        if percent_charged < 5 and not charging and self.notification:
            subprocess.Popen(['notify-send',
                              '--urgency=critical',
                              'Warning Low Battery'])

        response = {
            'full_text': full_text,
            'cached_until': self.py3.time_in(self.cache_timeout),
        }

        return response

    def on_click(self, i3s_output_list, i3s_config, event):
        """
        Display a notification with the remaining charge time.
        """
        if self.notification and self.time_remaining:
            subprocess.call(
                ['notify-send', '{}'.format(self.time_remaining), '-t', '4000'],
                stdout=open('/dev/null', 'w'),
                stderr=open('/dev/null', 'w')
            )

if __name__ == "__main__":
    from py3status.module_test import module_test
    module_test(Py3status)
