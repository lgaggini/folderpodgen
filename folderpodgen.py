import click
import glob
import os
import logging
import pytz
import re
from datetime import datetime
from podgen import Podcast, Episode, Media, Person, Category
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
@click.option('--author_name', required=True,
              help='the authors of the podcast')
@click.option('--author_email', help='the email of the podcast')
@click.option('--image', help='the url of the cover image for the podcast \
              (minimun 1400x1400px, jpg or png)')
@click.option('--feed_path', default='',
              help='the path of the podcast on website')
@click.option('--copyright', help='copyright informations')
@click.option('--language', default='en-EN',
              help='podcast language in ISO-639')
@click.option('--category', default='Music',
              help='podcast category')
@click.option('--blog/--no-blog', default=False,
              help='try to guess episode blog post')
@click.option('--blog_path', default='',
              help='path to blog posts')
@click.option('--verbose/--no-verbose', default=False,
              help='debug mode')
@click.argument('folder')
def generate(name, description, website, explicit, image, author_name,
             author_email, feed_path, copyright, language, category,
             blog, blog_path, verbose, folder):
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
    del attrs['feed_path']
    del attrs['blog']
    del attrs['blog_path']

    attrs['authors'] = [Person(author_name, author_email)]
    attrs['owner'] = attrs['authors'][0]

    attrs['category'] = Category(category)

    feed_name = name.lower().replace(' ', '_') + '.rss'
    feed_base = '%s/%s' % (website, feed_path)
    feed_url = '%s/%s' % (feed_base, feed_name)
    attrs['feed_url'] = feed_url

    logging.info('Creating podcast %s, feed %s' % (name, feed_url))
    p = Podcast(**attrs)

    for fpath in sorted(glob.glob('%s*.mp3' % (folder))):
        logging.info('Adding episode %s' % (fpath))
        fname = os.path.basename(fpath)
        size = os.path.getsize(fpath)
        logging.debug('Filename: %s, size %i' % (fname, size))
        try:
            tag = ID3(fpath)
        except ID3NoHeaderError:
            logging.error('%s is not a valid mp3 file, ignoring it' % (fpath))
            continue
        logging.debug('Read tag: %s' % (tag))
        e = Episode()
        if 'TPE1' in tag:
            e.authors = [Person(tag['TPE1'][0])]
        else:
            e.authors = attrs['authors']
        e.title = tag['TIT2'][0]
        e.subtitle = e.title
        if 'COMM::eng' in tag:
            e.summary = tag['COMM::eng'][0]
        else:
            e.summary = description
        episode_url = '%s/%s' % (feed_base, fname)
        logging.debug('Episode url: %s' % (episode_url))
        e.media = Media(episode_url, size, type='audio/mpeg')
        e.media.populate_duration_from(fpath)
        pubdate = datetime.strptime(tag['TDRC'][0].text, '%Y-%m-%d')
        pubdate = pubdate.replace(tzinfo=pytz.utc)
        e.publication_date = pubdate
        if blog:
            blog_post = ''
            short_name = re.search('[a-z]*_-_([a-z_]*[#0-9]*)', fname)
            if short_name:
                blog_post = short_name.group(1).replace('_', '-').\
                    replace('#', '') + '.html'
                e.link = '%s/%s/%s' % (website, blog_path, blog_post)
        p.episodes.append(e)

    feed_local_path = '%s%s' % (folder, feed_name)
    logging.info('Generating feed in %s' % (feed_local_path))
    p.rss_file(feed_local_path, minimize=False)


if __name__ == '__main__':
        generate()
