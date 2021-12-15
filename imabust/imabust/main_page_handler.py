import requests
from bs4 import BeautifulSoup

import re
from imabust.ph_logging import Logging

#log = Logging()


#links[] contains hotVideoSection href links 
#ex.links = ['/view_video.php?viewkey=ph615d68eb4bc6b', ...]

##  scrapes main page
### returns list of hrefs in hotvideosection
def get_all_hot_hrefs():
    r = requests.get(r'https://www.pornhub.com')
    links=[]
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        hvs = soup.find(id='hotVideosSection')
        a = hvs.find_all('a')

        rsearch = re.compile('^\/view_video.*')

        
        for link in a:
            rs = re.search(rsearch, link['href'])
            if rs:
                #print(link['href'])
                rgroup = rs.group()
                rgroup = 'https://www.pornhub.com' + rgroup
                
                if rgroup not in links:
                    links.append(rgroup)
                
        
    else:
        print("ERROR in Connection w/ Mainpage")
    
    log.add_log('mainPageHrefs', links)
    return links
    
    
   