#!/usr/bin/python3
# -*- coding: utf-8 -*-
import feedparser
import re
import subprocess
import uuid
import datetime
import os.path

ROOT_DIR = ''
DOWNLOAD_FILE = ROOT_DIR + '/downloaded'
REGEX_FILE = ROOT_DIR + '/regex'
RSS_FILE = ROOT_DIR + '/rss'
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

def get_rss_list(path):
   with open(path) as rss_file:
      rss_list = []
      for rss in rss_file:
         rss_list.append(rss)

   return rss_list

def get_regex_list(path, flags):
   with open(path) as regex_file:
      regex_list = []
      for regex_string in regex_file:
         regex_list.append(re.compile(regex_string.rstrip('\n'), flags))

   return regex_list


def get_download_link(entry):
   for link in entry.links:
      if link.type == "application/x-bittorrent":
         return link.href

   return entry.link[0].href

def download_torrent(entry, link, to_path):
   with open(LOG_FILE, 'a') as log_file:
      wget = subprocess.Popen(['wget',
                               link,
                               '--output-document=' + to_path + str(uuid.uuid4()) + '.torrent',
                               '--output-file=' + ROOT_DIR + '/wget_log'])
      wget.wait()
      if(wget.returncode == 0):
         log_file.write(str(datetime.datetime.now()) + ' Downloading: ' + entry.title + '\n')
      else:
         log_file.write(str(datetime.datetime.now()) + ' Error downloading: ' + entry.title + '\n')


def parse_rss(rss_list):
   for rss_url in rss_list:
      rss_feed = feedparser.parse(rss_url)
      regex_list = get_regex_list(REGEX_FILE, re.IGNORECASE)
      for regex in regex_list:
         for entry in rss_feed['entries']:
            match = regex.match(entry.title)
            if match and not torrent_already_downloaded(regex.pattern, match.group(1)):
               download_torrent(entry, get_download_link(entry), TORRENT_WATCH_DIR)
               add_to_downloaded_list(regex.pattern, match.group(1))

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

   rss_list = get_rss_list(RSS_FILE)
   parse_rss(rss_list)
