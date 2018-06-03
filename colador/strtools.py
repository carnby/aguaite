# coding: utf-8
from langid import langid
from cytoolz import keyfilter
from urllib.parse import urlparse
import unicodedata

def clean_id_strs(tweet):
    if type(tweet) == dict:
        tweet = keyfilter(lambda x: not x.endswith('id_str'), tweet)

        for key in tweet.keys():
            tweet[key] = clean_id_strs(tweet[key])

    elif type(tweet) == list:
        tweet = map(clean_id_strs, tweet)

    return tweet


def detect_language(text, threshold=0.9):
    classif = langid.classify(text)
    if not classif:
        return u'und'

    if classif[1] >= threshold:
        return classif[0]

    return 'und'


def add_domains(tweet):
    for url in tweet['entities']['urls']:
        expanded = url['expanded_url']
        if not expanded:
            expanded = url['url']
            url['expanded_url'] = expanded
        domain = urlparse(expanded).netloc

        if domain.startswith('www.'):
            domain = domain[4:]

        url['domain'] = domain


def remove_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def normalize_str(s, encoding='utf-8'):
    s = s.lower().strip()
    s = 'ñ'.join(map(remove_accents, s.split('ñ')))
    return s


def read_list_from_file(filename):
    with open(filename, 'r') as f:
        return list(map(lambda x: x, f.read().split('\n')))
