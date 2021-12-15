import requests, json
from bs4 import BeautifulSoup

import re
from imabust.main_page_handler import get_all_hot_hrefs
import subprocess
from imabust.ph_logging import Logging



class ScrapeAllPages:
    def __init__(self, links):
 
        self.links = links  #['link1', 'link2'...]
        self.hotspots = {} # {link, [hotspots]}
        self.mp4_names = {} #{link, mpr4name}
        self.r = re.compile('=ph.*')
        
        self.log = Logging(logfile = 'individual_page_scraper.txt', startup=True)
                
                #links saved as end of href.

    def init_downloads(self, vids_dir =r'.\imabust\vids', quality ='best'):
        ### external command used in runtime
        ### downloads vids to raw_vids        
        
        raw_vids_dir = vids_dir + '\\' + 'raw_vids'
        for i, link in enumerate(self.links):
            self.get_page_hotspots(link)
            self.mp4_names[link] = self.get_mp4_name(link)
            self.download_video(self.mp4_names[link], link, raw_vids_dir, quality)
                        
    def get_page_hotspots(self, link):
        ### scrapes link page. 
        ### sends page (request )text to parse_request
        ### updates self.hotspots with {link, [hotspots]}
        ### hotspots correspond to views in 5 second intervals
        
        r = requests.get(link)
        # print(link)
        # print(r.status_code)
        if r.status_code == 200:
            self.hotspots[link] = self.parse_request(r.text)
            
            print('scraped page: ' + link)
                
        else:
            print("ERROR in Connection: " + link)
            self.log.add_error(link)        

    def parse_request(self, text):
        #input raw request text
        #returns list of video hotspots [int1,int2, ...]}
        r = re.compile('"hotspots.*?]')
        
        rs = re.search(r, text)
        hotspots_raw = rs.group()    
        hotspots_raw = '{' + hotspots_raw + '}'   
        hotspots_dict = json.loads(hotspots_raw)

        hotspots = [int(x) for x in hotspots_dict['hotspots']]
        return hotspots 
    
    def get_mp4_name(self, link):
        ### external helper func
        rs = re.search(self.r, link)
        return rs.group()[1:]
        

    def do_log(self):
        self.log.add_log('mp4_names', self.mp4_names)
        self.log.add_log('hotspots', self.hotspots)


    def download_video(self, vid_name, link, raw_vids_dir, quality):
        ### helper func for init_downloads
        o = raw_vids_dir + '\\' + str(vid_name) + '.%(ext)s'
        self.log.add_log('youtube-dl_cmd', ['youtube-dl', link, '-i', '-w', '-o', o, '-f', quality])
        subprocess.run(['youtube-dl', link, '-i', '-w', '-o', o, '-f', quality])
        
