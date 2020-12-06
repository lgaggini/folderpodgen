# folderpodgen

folderpodgen is a Python script to generate a podcast RSS from a folder of mp3 files powered by [podgen](https://github.com/tobinus/python-podgen) and [mutagen](https://github.com/quodlibet/mutagen).

## Quickstart
```shell
folderpodgen --name mypodcast --description mypodcast --website "https://mypodcast.fm" --author_name "lgaggini"  /path/to/my/episodes/
```
## Features
* cli tool
* grabs episode informations from ID3:
    * artist -> artist
    * title -> title and subtitle
    * date (YYYY-MM-DD) -> publication date
    * comment -> description
    * duration -> duration
* powered by podgen and mutagen

## Install
```
git clone https://github.com/lgaggini/folderpodgen
cd folderpodgen
python setup.py install
```

pip package to come.

## Status
Beta version 0.2.0.

## Documentation
```shell
Usage: folderpodgen.py [OPTIONS] FOLDER

  Generate a podcast from mp3 files located in the provided FOLDER

Options:
  --name TEXT                 the name of the podcast  [required]
  --description TEXT          the description of the podcast  [required]
  --website TEXT              the url of the website of the podcast
                              [required]
  --explicit / --no-explicit  is the podcast explicit?
  --author_name TEXT          the authors of the podcast  [required]
  --author_email TEXT         the email of the podcast
  --image TEXT                the url of the cover image for the podcast
                              (minimun 1400x1400px, jpg or png)
  --feed_path TEXT            the path of the podcast on website
  --copyright TEXT            copyright informations
  --language TEXT             podcast language in ISO-639
  --category TEXT             podcast category
  --blog / --no-blog          try to guess episode blog post
  --blog_path TEXT            path to blog posts
  --verbose / --no-verbose    debug mode
  --help                      Show this message and exit.
```

