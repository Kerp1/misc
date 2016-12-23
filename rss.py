#!/usr/bin/python3
# -*- coding: utf-8 -*-
import feedparser
import re
import subprocess
import uuid
import datetime
import os.path

RSS_FEED = ''
ROOT_DIR = ''
DOWNLOAD_FILE = ROOT_DIR + '/downloaded'
REGEX_FILE = ROOT_DIR + '/regex'
LOG_FILE = ROOT_DIR + '/log.txt'
TORRENT_WATCH_DIR = ""


def torrent_already_downloaded(regex, episode):
   with open(DOWNLOAD_FILE, 'r') as downloaded_list:
      for downloaded in downloaded_list:
         if regex + ' ' + episode + '\n' == downloaded:
            return True

   return False

def add_to_downloaded_list(regex, episode):
   with open(DOWNLOAD_FILE, 'a') as downloaded_list:
      downloaded_list.write(regex + ' ' + episode + '\n')

def get_regex_list(path, flags):
   with open(path) as regex_file:
      regex_list = []
      for regex_string in regex_file:
         regex_list.append(re.compile(regex_string.rstrip('\n'), flags))

   return regex_list

def download_torrent(link, to_path):
   subprocess.Popen(['wget',
                       link,
                    '--output-document=' + to_path + str(uuid.uuid4()) + '.torrent',
                    '--output-file=' + ROOT_DIR + '/wget_log'])

def parse_rss(feed_url):
   log_file = open(LOG_FILE, 'a')
   rss_feed = feedparser.parse(feed_url)
   regex_list = get_regex_list(REGEX_FILE, re.IGNORECASE)
   for regex in regex_list:
      for entry in rss_feed['entries']:
         title = entry.title.encode('utf-8')
         match = regex.match(title)
         if match:
            print(title)
            if not torrent_already_downloaded(regex.pattern, match.group(1)):
               log_file.write(str(datetime.datetime.now()) + 'Downloading: ' + title + '\n')
               download_torrent(entry.links[0].href, TORRENT_WATCH_DIR)
               add_to_downloaded_list(regex.pattern, match.group(1))

   log_file.close()


def setup():
   if not os.path.isdir(ROOT_DIR):
      print("ROOT_DIR: " + ROOT_DIR + " doesn't exist")

   if not os.path.isdir(TORRENT_WATCH_DIR):
      print("TORRENT_WATCH_DIR: " + TORRENT_WATCH_DIR + " doesn't exist")

   open(REGEX_FILE, 'w')
   open(DOWNLOAD_FILE, 'w')

if __name__ == "__main__":
   if not os.path.exists(REGEX_FILE):
      setup()

   parse_rss(RSS_FEED)
