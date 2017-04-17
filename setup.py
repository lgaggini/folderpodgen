from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='folderpodgen',
    version='0.1',
    author_email='lg@lgaggini.net',
    url='https://github.com/lgaggini/drowse',
    license='LICENSE',
    py_modules=['folderpodgen'],
    keywords=['PODCAST', 'MP3', 'RSS'],
    description='Make a podcast RSS from a folder of MP3 files',
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta'
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    install_requires=[
         'click',
         'podgen',
         'mutagen',
    ],
    entry_points='''
        [console_scripts]
        folderpodgen=folderpodgen:generate
    ''',
)
