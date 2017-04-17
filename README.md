# folderpodgen

folderpodgen is a Python script to generate a podcast RSS from a folder of mp3 files powered by [podgen](https://github.com/tobinus/python-podgen) and [mutagen](https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore).

## Quickstart
```shell
folderpodgen --name mypodcast --description mypodcast --website "https://mypodcast.fm" --author_name "lgaggini"  /path/to/my/episodes/
```
## Features
* cli tool
* grab episode informations from ID3 (title, date, description (from comment tag) and duration)
* powered by podgen and mutagen

## Install
```
git clone https://github.com/lgaggini/folderpodgen
cd folderpodgen
python2 setup.py install
```

pip package to come.

## Status
Beta version 0.1.0, manual tested on a medium tests set.

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
  --author_name TEXT          the authors of the podcast
  --author_email TEXT         the email of the podcast
  --image TEXT                the url of the cover image for the podcast
                              (minimun 1400x1400px, jpg or png)
  --feed_url TEXT             the url of the podcast
  --copyright TEXT            copyright informations
  --verbose / --no-verbose    debug mode
  --help                      Show this message and exit.
```

