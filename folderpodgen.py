import click
import glob
import os
import logging
import pytz
from datetime import datetime
from podgen import Podcast, Episode, Media, Person
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError


@click.command()
@click.option('--name', required=True, help='the name of the podcast')
@click.option('--description', required=True,
              help='the description of the podcast')
@click.option('--website', required=True,
              help='the url of the website of the podcast')
@click.option('--explicit/--no-explicit', default=False,
              help='is the podcast explicit?')
@click.option('--author_name', help='the authors of the podcast')
@click.option('--author_email', help='the email of the podcast')
@click.option('--image', help='the url of the cover image for the podcast \
              (minimun 1400x1400px, jpg or png)')
@click.option('--feed_url', help='the url of the podcast')
@click.option('--copyright', help='copyright informations')
@click.option('--verbose/--no-verbose', default=False,
              help='debug mode')
@click.argument('folder')
def generate(name, description, website, explicit, image, author_name,
             author_email, feed_url, copyright, verbose, folder):
    """Generate a podcast from mp3 files located in the provided FOLDER"""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    attrs = locals()
    logging.debug('Processing input: %s' % (attrs))
    del attrs['folder']
    del attrs['author_name']
    del attrs['author_email']
    del attrs['verbose']

    if author_name or author_email:
        attrs['authors'] = [Person(author_name, author_email)]

    if not feed_url:
        feed_url = website

    logging.info('Creating podcast %s' % (name))
    p = Podcast(**attrs)

    for fpath in glob.glob('%s*.mp3' % (folder)):
        logging.info('Adding episode %s' % (fpath))
        fname = os.path.basename(fpath)
        try:
            tag = ID3(fpath)
        except ID3NoHeaderError:
            logging.error('%s is not a valid mp3 file, ignoring it' % (fpath))
            continue
        logging.debug('Read tag: %s' % (tag))
        e = Episode()
        e.title = tag['TIT2'][0]
        e.summary = tag['COMM::eng'][0]
        e.media = Media('%s/%s' % (feed_url, fname))
        e.media.populate_duration_from(fpath)
        pubdate = datetime.strptime(tag['TDRC'][0].text, '%Y-%m-%d')
        pubdate = pubdate.replace(tzinfo=pytz.utc)
        e.publication_date = pubdate
        e.link = '%s/%s' % (website, fname)
        p.episodes.append(e)

    feed_path = '%s%s.rss' % (folder, name.lower().replace(' ', '_'))
    logging.info('Generating feed in %s' % (feed_path))
    p.rss_file(feed_path, minimize=True)


if __name__ == '__main__':
        generate()
