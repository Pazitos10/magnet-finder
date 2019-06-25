import argparse
import requests
from bs4 import BeautifulSoup

AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'

def format_search_term(term):
    return term.replace(" ", "+")

def show_results(torrent_name, torrent_list):
    """Show results as a text formated table"""
    print("N°\t|SE\t|LE\t|Name")
    print("-"*32)
    for i, t in enumerate(torrent_list, 1):
        s = t["seeders"]
        l = t["leechers"]
        n = t["name"]
        print(f"{i}\t|{s}\t|{l}\t|{n}")
    print("-"*32)

def save_to_file(torrent_list, path, selection):
    """Saves the selected magnet link to a file"""
    name = torrent_list[selection]["name"]
    magnet = torrent_list[selection]["magnet"]
    magnet_file = f"{path}/magnet_{name}.txt"
    f = open(magnet_file, 'w')
    f.write(magnet)
    f.close()
    print(f"\"{name}\" magnet saved in: {magnet_file}! :D")
    print("The magnet file content is a kind of link, copy and paste it in your torrent client to start downloading.")

def remove_newline(a_list):
    return list(filter(lambda c: c != '\n', a_list))

def has_captcha(url):
    """Returns True if the page has a captcha or False otherwise."""
    results = requests.get(url, headers={'agent': AGENT})
    parsed_html = BeautifulSoup(results.text, 'html.parser')
    captcha = parsed_html.find_all('div', {'class': 'g-recaptcha'})
    return captcha

def get_magnet_from_details_page(url, detail_url):
    """Returns the magnet link from the details page"""    
    results = requests.get(url+detail_url, headers={'agent': AGENT})
    parsed_html = BeautifulSoup(results.text, 'html.parser')
    magnet = parsed_html.find_all('a', {'title': 'Get this torrent'})
    return magnet[0].get('href')

def get_torrent_matches(results):
    """Returns the data of the searched torrent if there are matches"""
    parsed_html = BeautifulSoup(results.text, 'html.parser')
    torrent_matches = parsed_html.find_all('div', {'class': 'detName'})
    best_magnet_copied = False
    torrent_list = []
    for tm in torrent_matches:
        ch = remove_newline(tm.parent.children)
        sl_count = remove_newline(tm.parent.next_siblings)
        seeders, leechers = list(map(lambda i: i.contents[0], sl_count))    
        name = ch[0].a.contents[0]
        magnet = ch[1].get('href')
        if not magnet.startswith('magnet:?xt='): 
            if not best_magnet_copied:
                magnet = get_magnet_from_details_page(mirror, magnet)
                best_magnet_copied = True #to avoid navigating when already has the best one copied
        data = {
            'seeders': seeders,
            'leechers': leechers,
            'name': name,
            'magnet': magnet 
        }
        torrent_list.append(data)
    return torrent_list

def search(mirror, term):
    """Performs the search on the main page."""
    term = format_search_term(term)
    url = f"{mirror}/s/?q={term}&category=0&page=0&orderby=99"
    if has_captcha(url):
        print("Cannot solve captcha :( Try with a different mirror URL using -m option")
    else:
        results = requests.get(url, headers={'agent': AGENT})
        return get_torrent_matches(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--torrent-name", help="torrent name")
    parser.add_argument("-p", "--path", help="destination folder for the magnet file", default=".")
    parser.add_argument("-f", "--save-to-file", help="saves the magnet link in a file", type=bool, default=False)
    parser.add_argument("-m", "--mirror", help="alternative mirror for tpb", default="https://thepiratebay.org")
    args = parser.parse_args()

    if args.torrent_name and args.path and args.mirror:
        torrent_name = args.torrent_name
        path = args.path
        mirror = args.mirror
        selection = None
        torrent_list = search(mirror, torrent_name)
        if not torrent_list:
            print(f"No results found for: \"{torrent_name}\" :(")
        else:
            show_results(torrent_name, torrent_list)
            first_torrent_name = torrent_list[0]["name"]
            first_torrent_magnet = torrent_list[0]["magnet"]
            print(f"The magnet link for \"{first_torrent_name}\" is: ")
            print(first_torrent_magnet)
            print("Use it on your torrent client app to start downloading.")
            if args.save_to_file:
                if selection is None:
                    selection = 0
                save_to_file(torrent_list, path, selection)
    else:
        print("TPBmf: Avoid the hassle and find the best magnet link for your torrents on your terminal!")
        parser.print_help()
