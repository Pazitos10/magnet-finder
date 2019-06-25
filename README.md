# TPBmf
#### TPB magnet finder
Avoid the hassle and find the best magnet link for your torrents on your terminal!

##### How to use:

1. Clone this repo (or Download it as ZIP): `git clone https://github.com/Pazitos10/tpbmf.git`
2. Install the dependencies:  `pip install -r requirements.txt`
3. Search for torrents: `python tpbmf -t "an awesome torrent name"`
4. Copy the magnet link to your clipboard and paste it on your torrent client open URL menu to start downloading.

##### More:

    $ python tpbmf -h
    usage: tpbmf.py [-h] [-t TORRENT_NAME] [-p PATH] [-s SHOW_FIRST]
                [-f SAVE_TO_FILE] [-m MIRROR]

    optional arguments:
      -h, --help            show this help message and exit
      -t TORRENT_NAME, --torrent-name TORRENT_NAME
                            torrent name
      -p PATH, --path PATH  destination folder for the magnet file
      -f SAVE_TO_FILE, --save-to-file SAVE_TO_FILE
                            saves the magnet link in a file
      -m MIRROR, --mirror MIRROR
                            alternative mirror for tpb

##### TODOs:
* [ ] Verify HTTP errors.
* [x] Work with multiple mirrors. 
* [ ] Allow the user to select which one to download.
* [ ] Support for pagination.
* [ ] Solve captchas.

##### Notes: This is a work in progress, you should not use it.