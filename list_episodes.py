import argparse
import requests
import os


def audio_drama_info(url):
    return requests.get(url).json()


def get_drama_name(audio_drama_info_json):
    return audio_drama_info_json['info']['drama']['name']


def create_out_dir(dir_name, parent_dir):
    dirPath = os.path.join(parent_dir, dir_name)
    if not os.path.isdir(dirPath):
        print('The directory is not present. Creating a new one..')
        os.mkdir(dirPath)
    else:
        print('The directory is present.')
    return dirPath


def get_episode_info(audio_drama_info_json, scrape_extras):
    episode = audio_drama_info_json['info']['episodes']['episode']
    names = []
    barrage_request_urls = []
    for e in episode:
        if scrape_extras:
            names.append(e['name'])
            barrage_request_urls.append("https://www.missevan.com/sound/getdm?soundid=" + str(e['sound_id']))
        elif not scrape_extras and e['name'][0] == '第':
            names.append(e['name'])
            barrage_request_urls.append("https://www.missevan.com/sound/getdm?soundid=" + str(e['sound_id']))
    return names, barrage_request_urls

def save_raw_barrage(names, urls):
    for n, u in zip(names, urls):
        f = open(n+".txt", mode="w", encoding='utf-8')
        #f.write(u)
        raw_barrage = requests.get(u)
        f.write(raw_barrage.text)
        f.close()



def main(request_url, extras, parent_dir, dir_name): #this runs when running from command line

    print('retriving audio drama info')
    json = audio_drama_info(request_url)

    # parse args / set defaults
    if not extras:
        extras = False
    if not parent_dir:
        parent_dir = os.curdir
    if not dir_name:
        dir_name = get_drama_name(json)

    print('creating new folder for scraped files')
    dirPath = create_out_dir(dir_name, parent_dir)
    os.chdir(dirPath)
    [episode_names, barrage_request_urls] = get_episode_info(json, extras)
    save_raw_barrage(episode_names, barrage_request_urls)

def parse_args():
    example_text = '''example:

        Scrape all QJJ S1 episodee, no extras
         python list_episodes.py -o C:\\Users\\test\\Downloads\\ https://www.missevan.com/dramaapi/getdramabysound?sound_id=2121328
         Scrape all QJJ S1 episodes + extras
         python list_episodes.py https://www.missevan.com/dramaapi/getdrama?drama_id=25944 --incl_extras -d QJJS1
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("request_url",
                        help="request URL from MaoErFM containing all episode URLs, usually getdramabysound or getdrama")
    parser.add_argument("--incl_extras", "-e", help="include -e to scrape extras in addition to episode", default=False, action='store_true')
    parser.add_argument("--output_dir", "-o", help="output directory path")
    parser.add_argument("--directory", "-d", help="directory name for scraped files. Default is current directory.")
    #parser.add_argument(description='scrape MarErFM subs', epilog=example_text)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args.request_url, args.incl_extras, args.output_dir, args.directory)

