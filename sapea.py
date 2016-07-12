# -*- coding: utf-8 -*-
import time
import datetime
import logging
import tweepy
import sys
import gzip
import os

try:
    import ujson as json
except ImportError:
    import json

from colador import normalize_str, remove_accents, read_list_from_file

class Listener(tweepy.StreamListener):
    def __init__(self, fd, time_limit):
        '''

        :param fd: a file handle
        :param time_limit: in seconds
        :return:
        '''
        self.fd = fd
        self.time_limit = time_limit
        self.start_time = time.time()
        super(tweepy.StreamListener, self).__init__()

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_data(self, data):
        print(repr(data))
        self.fd.write(data)
        delta_time = time.time() - self.start_time

        if delta_time >= self.time_limit:
            return False
        return True

if __name__ == '__main__':
    auth = None
    options = None
    api = None

    with open('config.json', 'r') as f:
        options = json.load(f)
        logging.basicConfig(level=options['log_level'])
        logging.debug(options)

    if options is None:
        logging.error('No valid options.')
        sys.exit(1)

    with open('keys.json', 'r') as f:
        api_keys = json.load(f)
        auth = tweepy.OAuthHandler(api_keys['consumer_key'], api_keys['consumer_secret'])
        auth.set_access_token(api_keys['access_token_key'], api_keys['access_token_secret'])
        api = tweepy.API(auth)

    if auth is None:
        logging.error('No valid authentication keys.')
        sys.exit(1)

    path = options['storage_path']
    project_path = options['project_data_path']

    keywords = read_list_from_file('{0}/keywords.txt'.format(project_path))
    keywords = filter(lambda x: x and x[0] != '%' and 1 < len(x) < 60, keywords)
    keywords = list(map(normalize_str, keywords))
    keywords = keywords[0:125]
    logging.debug(keywords)

    locations = options['search_location_box']
    time_limit = int(options['minutes'] * 60)
    logging.debug('time limit in minutes', time_limit)

    start_time = time.time()
    now = datetime.datetime.now().strftime("%Y%m%d%H%M")
    filename = '{0}/{1}_{2}.data.gz'.format(path, options['project_name'], now)

    if options['source_account']:
        people = list(map(str, api.friends_ids(screen_name=options['source_account'])))
        logging.debug(people)
    else:
        people = None

    with gzip.open(filename + '.part', 'wt') as f:
        listener = Listener(f, time_limit)
        stream = tweepy.Stream(auth, listener)
        stream.filter(track=keywords, follow=people, locations=locations)

    os.rename(filename + '.part', filename)
