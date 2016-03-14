# coding: utf-8
from __future__ import unicode_literals, print_function
import os
import glob
import gzip
try:
    import ujson as json
except ImportError:
    import json
import codecs
import colador
import argparse

if __name__ == '__main__':
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

    args = parser.parse_args()

    print(args)

    sources = glob.glob(args.source)
    prefix = args.prefix
    storage = args.store
    project_path = args.project

    print(sources)

    for source in sources:
        target = source.split('/')[-1]

        if os.path.exists('{0}/{1}_stats.json'.format(storage, target)):
            print(target, 'exists')
            continue

        files = glob.glob('{0}/{1}*.gz'.format(source, prefix))
        files.sort()

        if args.debug:
            # just 10 files in debug mode
            files = files[:10]

        col = colador.Colador(data_path=project_path)

        if not args.debug:
            target_file = '{1}/{0}_consolidated.json.gz'.format(target, storage)
        else:
            target_file = '{0}/debug.json.gz'.format(storage)

        with gzip.open(target_file, 'wb') as dst:
            for i, filename in enumerate(files):
                try:
                    with gzip.open(filename, 'r') as src:
                        for line in src:
                            try:
                                tweet = json.loads(line.decode('utf-8'))
                            except ValueError:
                                print('valueerror', line)
                                continue

                            try:
                                if col.accept_tweet(tweet):
                                    col.prepare_and_write(dst, tweet)
                            except TypeError as e:
                                print('typeerror', e, tweet)
                                continue
                except IOError:
                    print(filename, 'invalid')
                    continue

                if i % 100 == 0:
                    print('{0} - {1} tweets and counting. source: {2}'.format(target, col.total_tweet_count, filename))

        stats = {'target': target, 'total_tweets': col.total_tweet_count,
             'discarded_sources': list(col.discarded_sources.most_common(10)),
             'reject_reasons': list(col.reject_reasons.items())
        }

        if args.debug:
            print(stats)
            break

        with codecs.open('{0}/{1}_stats.json'.format(storage, target), 'w', 'utf-8') as f:
            json.dump(stats, f)
            print(stats)
