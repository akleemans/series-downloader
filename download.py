#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Checks the progress of user-defined TV series and gathers links of the missing episodes.

'''

import os
import urllib2
import webbrowser
import time

def download(url):
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    time.sleep(1) # slow it down a bit
    return data
    
def calculate_delta(newest_available, latest):
    delta = []
    for i in range(newest_available + 1, int(latest[3:5])+1):
        delta.append('S' + latest[:2] + 'E' + ('0' + str(i))[-2:])
    
    return delta
    
def main():
    f = open('series.txt', 'r')
    content = f.read()
    f.close()
    series = content.split('\n')
    del series[-1]
    
    print 'Found', len(series), 'series.'
    os.chdir('.')
    
    for serie in series:
        # get current episode
        print '\nChecking tvrage.com for "' + serie + '"...'
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
        for f in os.listdir(path):
            if f.endswith(".mp4"):
                episodes.append(f)

        numbers = [0]
        for episode in episodes:
            key = 'S' + latest[0:2] + 'E'
            if key in episode:
                n = int(episode[episode.find(key)+4:episode.find(key)+6])
                numbers.append(n)
                
        newest_available = max(numbers)
        print 'Newest available episode:', newest_available
        
        urls = calculate_delta(newest_available, latest)
        if len(urls) == 0:
            print 'Up-to-date.'
        else:
            print 'Starting downloads for', len(urls), 'episodes...'
        
        # download missing episodes
        for episode in urls:
            url = 'http://thepiratebay.se/search/' + (serie + ' ' + episode).replace(' ', '%20') + '/0/7/0'
            site = download(url)
            
            # filter torrent link and open in browser
            site = site[site.find('magnet'):]
            url = site[:site.find('"')]
            webbrowser.open(url)
        
    print '\nFinished.'
        
if __name__ == "__main__":
    main()
