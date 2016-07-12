# coding: utf-8
from __future__ import unicode_literals, print_function
import os
import glob
import gzip
import logging
import codecs
import colador
import argparse

try:
    import ujson as json
except ImportError:
    import json


if __name__ == '__main__':
    options = None

    with open('config.json', 'r') as f:
        options = json.load(f)
        logging.basicConfig(level=options['log_level'])
        logging.debug(options)

    if options is None:
        logging.error('No valid options.')
        sys.exit(1)

    prefix = options['project_name']
    source_storage = options['storage_path']
    target_storage = options['filtered_path']
    project_path = options['project_data_path']

    sources = glob.glob('{0}/{1}_*.gz'.format(source_storage, prefix))
    logging.info(sources)

    col = colador.Colador(data_path=project_path)

    for source in sources:
        filename = source.split('/')[-1]

        if os.path.exists('{0}/{1}.stats.json'.format(target_storage, filename)):
            logging.info('{0} already processed'.format(filename))
            continue

        target_file = '{0}/{1}'.format(target_storage, filename)

        with gzip.open(target_file, 'wb') as dst:
            try:
                with gzip.open(source, 'r') as src:
                    for line in src:
                        try:
                            tweet = json.loads(line.decode('utf-8'))
                        except ValueError as e:
                            logging.error(str(e))
                            logging.error(line)
                            continue

                        try:
                            if col.accept_tweet(tweet):
                                col.prepare_and_write(dst, tweet)
                        except TypeError as e:
                            logging.error(str(e))
                            logging.error(tweet)
                            continue
            except IOError:
                logging.error('invalid source file')
                logging.error(source)
                continue


            stats = {
                'source_file': source,
                'total_tweets': col.total_tweet_count,
                'discarded_sources': list(col.discarded_sources.most_common(10)),
                'reject_reasons': list(col.reject_reasons.items())
            }

            with open('{0}/{1}.stats.json'.format(target_storage, filename), 'w') as f:
                json.dump(stats, f)
                logging.debug(stats)
