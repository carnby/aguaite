# coding: utf-8
from collections import Counter
from cytoolz import keyfilter, memoize
from .strtools import *
import re
import codecs
import pytz
import datetime
import ujson as json

__author__ = 'egraells'


class Colador(object):
    def __init__(self, data_path):
        self.total_tweet_count = 0
        # we remember.
        self.saved_tweets = set()

        self.res = {
            'hashtag': re.compile(r'#([\w]+)'),
            'mention': re.compile(r'@([\w]+)'),
            'phrase': re.compile('[^\s\d\w]'),
            'split': re.compile(r'[\W\s]+'),
            'non_word': re.compile('[\W]+'),
            'spaces': re.compile('\s+'),
            'url': re.compile(r'(https?://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|])')
        }

        self.new_line = '\n'.encode('utf-8')

        self.accepted_languages = {'es'}

        self.allowed_keys = {'truncated', 'text', 'in_reply_to_status_id', 'id', 'favorite_count',
                'source', 'retweeted', 'coordinates', 'entities', 'in_reply_to_screen_name',
                'retweet_count', 'in_reply_to_user_id', 'user',
                'lang', 'created_at', 'retweeted_status_id', 'quoted_status_id'}

        self.allowed_user_keys = {"profile_use_background_image", "default_profile_image", "id", "verified",
                             "profile_image_url_https", "profile_sidebar_fill_color", "profile_text_color",
                             "followers_count", "profile_sidebar_border_color", "profile_background_color",
                             "listed_count", "profile_background_image_url_https", "utc_offset", "statuses_count",
                             "description", "friends_count", "location", "profile_link_color", "profile_image_url",
                             "following", "profile_banner_url", "profile_background_image_url",
                             "name", "lang", "profile_background_tile", "favourites_count", "screen_name",
                             "url", "created_at", "time_zone", "protected", "default_profile"}

        self.allowed_entities = {'media', 'hashtags', 'user_mentions', 'urls'}

        with codecs.open('{0}/discard_locations.txt'.format(data_path), 'r', 'utf-8') as f:
            self.discarded_locations = set(map(self.prepare_location_name, f.read().split('\n')))

        with codecs.open('{0}/discard_keywords.txt'.format(data_path), 'r', 'utf-8') as f:
            self.discard_keywords = set(map(normalize_str, f.read().split('\n')))
            self.discard_hashtags = set(w[1:] for w in self.discard_keywords if w[0] == '#')
            self.discard_mentions = set(w[1:] for w in self.discard_keywords if w[0] == '@')

        with codecs.open('{0}/discard_urls.txt'.format(data_path), 'r', 'utf-8') as f:
            self.discarded_urls = set(f.read().split('\n'))

        with codecs.open('{0}/twitter_time_zones.csv'.format(data_path), 'r', 'utf-8') as f:
            self.zone_dict = {}
            # Santiago => (GMT-04:00)
            for l in f:
                parts = l.strip().split(',', 2)
                self.zone_dict[parts[1]] = parts[0]

        with codecs.open('{0}/allowed_time_zones.txt'.format(data_path), 'r', 'utf-8') as f:
            self.allowed_timezones = set(f.read().split('\n'))
            # self.allowed_timezones = {'(GMT-03:00)', '(GMT-04:00)'}

        with codecs.open('{0}/discard_time_zones.txt'.format(data_path), 'r', 'utf-8') as f:
            self.discarded_timezones = set(f.read().split('\n'))
            # {'Brazilia', 'Brasilia', 'Georgetown', 'Greenland', 'Atlantic Time (Canada)'}

        with codecs.open('{0}/allowed_sources.txt'.format(data_path), 'r', 'utf-8') as f:
            self.allowed_sources = set(f.read().split('\n'))

        self.discarded_sources = Counter()
        self.reject_reasons = Counter()

        self.twitter_date_format = '%a %b %d %H:%M:%S +0000 %Y'
        self.target_date_format = '%Y-%m-%d %H:%M:%S'

    def is_present(self, tweet):
        return tweet['id'] in self.saved_tweets

    def write_tweet(self, f, tweet):
        tweet = clean_id_strs(tweet)
        self.prepare_tweet(tweet)

        tweet = keyfilter(lambda x: x in self.allowed_keys, tweet)
        tweet['entities'] = keyfilter(lambda x: x in self.allowed_entities, tweet['entities'])

        #print(tweet['user']['screen_name'], tweet['text'])
        #print(json.dumps(tweet))
        f.write(json.dumps(tweet, ensure_ascii=False).encode('utf-8'))
        f.write(self.new_line)

        self.total_tweet_count += 1
        self.saved_tweets.add(tweet['id'])

    def prepare_and_write(self, f, tweet):
        """
        Writes a tweet (and potentially nested tweets).
        Before writing, it checks the tweet has not been added before.
        """
        if 'retweeted_status' in tweet and tweet['retweeted_status']:
            if not self.is_present(tweet['retweeted_status']):
                #print('RT')
                self.prepare_and_write(f, tweet['retweeted_status'])
            #else:
            #    print('RT already added')
        if 'quoted_status' in tweet and tweet['quoted_status']:
            if not self.is_present(tweet['quoted_status']):
                #print('QUOTE')
                self.prepare_and_write(f, tweet['quoted_status'])
            #else:
            #    print('QUOTE already added')
        #print('REG')
        if not self.is_present(tweet):
            self.write_tweet(f, tweet)

    def prepare_location_name(self, text):
        if text is None:
            return ''

        text = normalize_str(text)
        # Mexico D.F. => Mexico DF
        text = text.replace('.', '')
        text = text.replace(',', ' ')
        # Remove hashes, hearts, etc
        text = self.res['non_word'].sub(' ', text)
        text = self.res['spaces'].sub(' ', text)
        return text.strip()

    @memoize
    def is_valid_timezone(self, time_zone_name):
        if time_zone_name in self.allowed_timezones:
            #print('OK', time_zone_name)
            return True

        if time_zone_name not in self.zone_dict:
            #print('Rejected! Unknown time zone', time_zone_name)
            return False

        if self.zone_dict[time_zone_name] not in self.allowed_timezones or time_zone_name in self.discarded_timezones:
            #print('Rejected! Discarded time zone', time_zone_name)
            return False

        #print(self.allowed_timezones)
        #print(self.discarded_timezones)
        #print('OK', time_zone_name, self.zone_dict[time_zone_name] if time_zone_name else None)
        return True

    def accept_tweet(self, tweet, check_repeated=True, check_sources=True, check_time_zone=True):
        if 'text' not in tweet:
            #print('invalid tweet')
            self.reject_reasons['invalid'] += 1
            return False

        if self.is_present(tweet):
            if check_repeated:
                self.reject_reasons['repeated'] += 1
                return False
            # since we do not check repeats, and it is available, we accept it immediately.
            return True

        if check_sources and tweet['source'] not in self.allowed_sources:
            #print('rejected! source: {0}'.format(tweet['source']))
            self.reject_reasons['blacklisted_source'] += 1
            self.discarded_sources[tweet['source']] += 1
            return False

        time_zone = tweet['user'].get('time_zone', None)
        if check_time_zone and not self.is_valid_timezone(time_zone):
            self.reject_reasons['time_zone'] += 1
            return False

        if 'retweeted_status' in tweet and tweet['retweeted_status']:
            # we don't check sources for retweets, nor if it was added
            accepted = self.accept_tweet(tweet['retweeted_status'], check_repeated=False, check_sources=False, check_time_zone=False)
            if not accepted:
                self.reject_reasons['rejected_rt'] += 1
                #print(u'Rejected RT!')
                return False

        if 'quoted_status' in tweet and tweet['quoted_status']:
            # we don't check sources for quotes, nor if it was added
            accepted = self.accept_tweet(tweet['quoted_status'], check_repeated=False, check_sources=False, check_time_zone=False)
            if not accepted:
                self.reject_reasons['rejected_quote'] += 1
                #print(u'Rejected Quote!')
                return False

        if not 'lang' in tweet:
            tweet['lang'] = detect_language(tweet['text'])

        if not tweet['lang'] in self.accepted_languages:
            #print('invalid language', tweet['lang'])
            self.reject_reasons['language'] += 1
            return False

        screen_name = tweet['user']['screen_name'].lower()
        if screen_name in self.discard_mentions:
            #print('Rejected! Blacklisted user: {0}'.format(screen_name))
            self.reject_reasons['blacklisted_user'] += 1
            return False

        if 'hashtags' in tweet['entities'] and tweet['entities']['hashtags']:
            for h in tweet['entities']['hashtags']:
                if normalize_str(h['text']) in self.discard_hashtags:
                    #print(u'Rejected! Hashtags: {0}'.format(h['text']))
                    self.reject_reasons['blacklisted_hashtag'] += 1
                    return False

        if 'user_mentions' in tweet['entities'] and tweet['entities']['user_mentions']:
            #mentions = set('@{0}'.format(h['screen_name'].lower()) for h in tweet['entities']['user_mentions'])
            for m in tweet['entities']['user_mentions']:
                if m['screen_name'].lower() in self.discard_mentions:
                    #print(u'Rejected! Mentions: {0}'.format(m['screen_name']))
                    self.reject_reasons['blacklisted_mention'] += 1
                    return False

        if 'urls' in tweet['entities'] and tweet['entities']['urls']:
            add_domains(tweet)
            #domains = set(pluck('domain', tweet['entities']['urls']))
            for u in tweet['entities']['urls']:
                if u['domain'] in self.discarded_urls:
                    #print(u'Rejected! URLs: {0}'.format(u['domain']))
                    self.reject_reasons['blacklisted_domain'] += 1
                    return False

        if tweet['user']['location'] and self.prepare_location_name(tweet['user']['location']) in self.discarded_locations:
            #print('invalid location', tweet['user']['location'])
            self.reject_reasons['location'] += 1
            return False

        return True

    def prepare_user(self, user):
        user['created_at'] = self.parse_twitter_date(user['created_at'])

        if not 'profile_banner_url' in user:
            user['profile_banner_url'] = None

        keys = list(user.keys())

        for key in keys:
            if not key in self.allowed_user_keys:
                del user[key]

        for key in self.allowed_user_keys:
            if not key in user:
                print('warning: missing user key', key)

    def prepare_tweet(self, tweet):
        self.prepare_user(tweet['user'])

        # timestamps
        tweet['created_at'] = self.parse_twitter_date(tweet['created_at'])

        # geo
        lat = None
        lon = None

        if 'geo' in tweet and tweet['geo']:
            coords = tweet['geo'].get('coordinates', None)
            geo_type = tweet['geo'].get('type', None)
            if coords and geo_type and geo_type == 'Point':
                lat, lon = coords
            del tweet['geo']

        elif 'coordinates' in tweet and tweet['coordinates']:
            coords = tweet['coordinates'].get('coordinates', None)
            geo_type = tweet['coordinates'].get('type', None)
            if coords and geo_type and geo_type == 'Point':
                lon, lat = coords
            del tweet['coordinates']

        if 'coordinates' in tweet:
            del tweet['coordinates']

        if 'geo' in tweet:
            del tweet['geo']

        tweet['coordinates'] = {'lat': lat, 'long': lon}

        # retweets
        if 'retweeted_status' in tweet:
            tweet['retweeted_status_id'] = tweet['retweeted_status']['id']
        else:
            tweet['retweeted_status_id'] = None

        # quotes
        if 'quoted_status_id' not in tweet:
            tweet['quoted_status_id'] = None

        for key in self.allowed_keys:
            if not key in tweet:
                print('warning: missing key', key)


    def parse_twitter_date(self, text):
        naive_datetime = datetime.datetime.strptime(text, self.twitter_date_format).replace(tzinfo=pytz.UTC)
        #dt = pytz.timezone(PYTZ_TIMEZONE).localize(naive_datetime)
        return naive_datetime.strftime(self.target_date_format)
