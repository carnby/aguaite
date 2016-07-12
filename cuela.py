# coding: utf-8
from __future__ import unicode_literals, print_function
import os
import glob
import gzip
import logging
try:
    import ujson as json
except ImportError:
    import json
import codecs
import colador
import argparse

if __name__ == '__main__':
    options = None

    with open('config.json', 'r') as f:
        options = json.load(f)
        logging.basicConfig(level=options['log_level'])
        logging.debug(options)

    if options is None:
        logging.error('No valid options.')
        sys.exit(1)


    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix', help='File prefix used in crawled files. Example: general', default='general_2014_')
    parser.add_argument('--store', help='Path to folder used to store consolidated files.',
        default='/media/egraells/113A88F901102CA6/data/aurora/consolidated/')
    parser.add_argument('--source', help='Path to folders containing compressed tweets (e.g., 201409). Wildcards can be used.',
        default='/media/egraells/113A88F901102CA6/data/aurora/stream-data/*')
    parser.add_argument('--project', help='Path to the project folder.',
        default='/home/egraells/resources/aurora/projects/cl')
    parser.add_argument('--debug', help='Flag to execute the loop only once, without saving results.', action='store_true',
        default=False)

    prefix = options['project_name']
    source_storage = options['storage_path']
    target_storage = options['filtered_path']
    project_path = options['project_data_path']

    sources = glob.glob('{0}/{1}_*.gz'.format(source_storage, prefix))
    logging.info(sources)

    for source in sources:
        filename = source.split('/')[-1]

        if os.path.exists('{0}/{1}.stats.json'.format(target_storage, filename)):
            logging.info(filename, 'was processed')
            continue

        col = colador.Colador(data_path=project_path)

        target_file = '{0}/{1}'.format(target_storage, filename)

        with gzip.open(target_file, 'wb') as dst:
            try:
                with gzip.open(source, 'r') as src:
                    for line in src:
                        try:
                            tweet = json.loads(line.decode('utf-8'))
                        except ValueError as e:
                            logging.error(e)
                            logging.error(line)
                            continue

                        try:
                            if col.accept_tweet(tweet):
                                col.prepare_and_write(dst, tweet)
                        except TypeError as e:
                            logging.error(e)
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
