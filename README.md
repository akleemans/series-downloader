series-downloader
=================

Downloads the latest episodes of your favorite TV show.

## Prerequisites

 * Python
 * a BitTorrent-client
 * a browser which automatically redirects magnet-links to the BitTorrent-client

## Usage
Specify your favorite TV series in *series.txt* and start the downloader by typing 	

	python download.py

It will automatically download the latest episodes of the specified series (of the current season).

For each TV show, a separate folder is created, and after downloading you should put the files there, so that the script can recognize what's missing.

## How it works
For each show, a query to http://www.tvrage.com/ is sent to check the latest episode.
The exact URL is `http://services.tvrage.com/tools/quickinfo.php?show=[name of show]`, which returns some text with information about the show.

Then, the script looks up if there are any episodes already there, and if the latest episode is there, it finishes.

If there's any difference between the latest episode and the newest episode the user has, a query to PirateBay is sent.
The URL is `'http://thepiratebay.se/search/[name of show and season/episode name]/0/7/0'`, so the results are sorted for seeders.

The first magnet-link (usually the one with the most seeders) is then extracted and 

The script itself does not download any torrent, it just searches for the right torrent/magnet links and opens them in the standard web browser.

## Disclaimer
As said, the script itself does not download any torrent files, it just opens the standard web browser with the magnet-link.
Be aware that by executing this script, torrent files will be added to your BitTorrent client for downloading.

The script is provided "as is" without warranty of any kind.
