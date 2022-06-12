import argparse
from requests import get
from requests.utils import quote

def show_results(search_terms, torrent_list):
    """Show results as a text formated table"""
    line_length = 100
    line_str = "-"*line_length
    print(f'Results for: "{search_terms}" - ({len(torrent_list)} results)')
    print("N°\t| SE\t| LE\t| Size\t| Category\t| Name")
    print(line_str)
    for i, t in enumerate(torrent_list, 1):
        s = t["seeders"]
        l = t["leechers"]
        n = t["name"]
        z = t["size"]
        c = t["category"]
        print(f"{i}\t| {s}\t| {l}\t| {z}\t| {c}\t| {n}")
    print(line_str)

def save_to_file(magnet, filename):
    """Saves the selected magnet link to a file"""
    with open(filename, 'w') as f:
        f.write(magnet)
        print(f"\"{name}\" magnet saved in: {filename}! :D")
        print("Open it (or copy and paste its content) in your torrent client to start the download process.")

def append_trackers():
    """Returns the base tracker list"""
    trackers = [
        'udp://tracker.coppersurfer.tk:6969/announce',
        'udp://tracker.openbittorrent.com:6969/announce',
        'udp://9.rarbg.to:2710/announce',
        'udp://9.rarbg.me:2780/announce',
        'udp://9.rarbg.to:2730/announce',
        'udp://tracker.opentrackr.org:1337',
        'http://p4p.arenabg.com:1337/announce',
        'udp://tracker.torrent.eu.org:451/announce',
        'udp://tracker.tiny-vps.com:6969/announce',
        'udp://open.stealth.si:80/announce',
    ]
    trackers = [quote(tr) for tr in trackers]
    return '&tr='.join(trackers)

def category_name(category):
    """Translates the category code to a name"""
    names = [
        '',
        'audio',
        'video',
        'apps',
        'games',
        'nsfw',
        'other'
    ]
    category = int(category[0])
    category = category if category < len(names) - 1 else -1
    return names[category]

def size_as_str(size):
    """Formats the file size in bytes to kb, mb or gb accordingly"""
    size = int(size)
    size_str = f"{size} b"
    if size >= 1024:
        size_str = f"{(size / 1024):.2f} kb"
    if size >= 1024 ** 2:
        size_str = f"{(size / 1024 ** 2):.2f} mb"
    if size >= 1024 ** 3:
        size_str = f"{(size / 1024 ** 3):.2f} gb"
    return size_str

def magnet_link(ih, name):
    """Creates the magnet URI"""
    return f'magnet:?xt=urn:btih:{ih}&dn={quote(name)}&tr={append_trackers()}'

def torrent_matches(results):
    """Returns the data of the searched torrent if there are matches"""
    matches = []
    if results.status_code == 200:
        data = results.json()
        if data and 'no results' in data[0]['name'].lower():
            return matches
        for d in data:
            matches.append({
                'seeders': d['seeders'],
                'leechers': d['leechers'],
                'name': d['name'],
                'category': category_name(d['category']),
                'size': size_as_str(d['size']),
                'magnet': magnet_link(d['info_hash'], d['name']),
            })
    return matches

def search(terms):
    """Searches torrents with the given terms."""
    agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0'
    url = f"https://apibay.org/q.php?q={quote(terms)}"
    results = get(url, headers={'agent': agent})
    return torrent_matches(results)

def select_option(n_results):
    """Handles the user option selection prompt and returns the selected option (default = 1)"""
    option = 0
    try:
        option = int(input("Choose one of the results to get the magnet link: "))
    except ValueError:
        print("No option selected, default is 1.")
    except KeyboardInterrupt:
        print("\nYou never saw me.")
        exit()
    if option < 0 or option > n_results:
        print("Incorrect option selected, default is 1.")
        option = 0
    elif option > 0:
        option = option - 1
    return option

def main(search_terms, filename=None):
    results = search(search_terms)
    if not results:
        print(f"No results found for: \"{search_terms}\" :(")
    else:
        show_results(search_terms, results)
        option = select_option(len(results))
        name = results[option]["name"]
        magnet = results[option]["magnet"]
        print(f"The magnet link for \"{name}\" is: \n\n{magnet}\n")
        print("Use it on your torrent client app to start downloading.")
        if filename:
            save_to_file(magnet, filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search-terms", help="use double quotes to indicate the search terms")
    parser.add_argument("-f", "--file", help="save your magnet link to a file")
    args = parser.parse_args()

    if args.search_terms:
        main(args.search_terms, args.file)
    else:
        print("magnet-finder: Skip the ads and find the best magnet links for your torrents on your terminal!")
        parser.print_help()
