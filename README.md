# magnet-finder
#### magnet finder
Skip the ads and find the best magnet links for your torrents on your terminal!

##### How to use:

1. Clone this repo (or Download it as ZIP): `git clone https://github.com/Pazitos10/magnet-finder.git`
2. Install the dependencies:  `pip install -r requirements.txt`
3. Search for torrents: `python magnet-finder.py -s "awesome search terms"`
4. Copy the magnet link to your clipboard and paste it on your torrent client open URL menu to start downloading.

##### More:

    $ python magnet-finder.py -h
    usage: magnet-finder.py [-h] [-s SEARCH_TERMS] [-f FILE]

    options:
      -h, --help            show this help message and exit
      -s SEARCH_TERMS, --search-terms SEARCH_TERMS
                            use double quotes to indicate the search terms
      -f FILE, --file FILE  save your magnet link to a file

##### TODOs:
* [x] Allow the user to select which one to download.
* [ ] Filter by categories.

##### Notes: This is a work in progress, you should not use it.
