import os
import urllib2
import webbrowser
import time

def download(url):
    print 'Downloading', url
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    time.sleep(1)
    
    return data
    
def download2(url):
    page = ''
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    data = ''
    req = urllib2.Request(url, data, headers)
    try:
        page = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        page = e.fp.read()

    return page
    
def calculate_delta(newest_available, latest):
    delta = []
    for i in range(newest_available + 1, int(latest[:2])+1):
        if i < 10:
            s = '0' + str(i)
        else:
            s = str(i)
        delta.append('S' + latest[:2] + 'E' + s)
    
    return delta
    
def main():
    f = open('series.txt', 'r')
    content = f.read()
    f.close()
    series = content.split('\n')
    del series[-1]
    
    print 'Found', len(series), 'series.'
    
    for serie in series:
        # get current episode
        print 'Checking tvrage.com for "' + serie + '"...'
        url = 'http://services.tvrage.com/tools/quickinfo.php?show=' + serie.replace(' ', '%20')
        site = download(url)
        idx = site.find('Latest Episode@') + 15
        latest = site[idx:idx+5]
        print 'Latest episode:', latest
        
        # check how many already there
        path = './' + serie
        if not os.path.exists(path):
            print 'Creating directory "' + serie + '"'
            os.makedirs(path)
        
        episodes = []
        os.chdir(path)
        for f in os.listdir("."):
            if f.endswith(".avi"):
                episodes.append(f)
        
        numbers = [0]
        for episode in episodes:
            if 'S' + latest[:2] + 'E' in episode:
                n = int(episode[episode.find()+4:episode.find()+6])
                numbers.append(n)

        newest_available = max(numbers)
        print 'Newest available episode:', newest_available
        
        urls = calculate_delta(newest_available, latest)
        
        # download missing episodes
        for episode in urls:
            url = 'http://thepiratebay.se/search/' + (serie + ' ' + episode).replace(' ', '%20') + '/0/7/0'
            print 'Starting download for episode', episode
            site = download(url)
            
            # filter torrent link
            site = site[site.find('magnet'):]
            url = site[:site.find('"')]

            #webbrowser.open(url)
    
if __name__ == "__main__":
    main()
