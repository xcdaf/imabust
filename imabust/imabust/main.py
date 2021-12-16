
from imabust.movie_page_handler import ScrapeAllPages
from imabust.main_page_handler import get_all_hot_hrefs
from imabust.hotspot_calculations  import DFHandler
from imabust.video_handler import VideoHandler
from imabust.ph_logging import Logging
from imabust import formulas
from datetime import datetime
import json


#Settings ###############################

VIDSDIR = r'.\imabust\vids'
FORMULA = formulas.rolling
KWARGS = {'window': 20,
            'std': 1}

HS_PATH = r'.\imabust\tests\individual_page_scraper.txt'
#l = 'https://www.pornhub.com/view_video.php?viewkey='
# TEST_FILE = 'ph61658be992234'
# PH_LINK = l+TEST_FILE
########################################



def run_main(vids_dir = VIDSDIR,
        formula = FORMULA,
        kwargs = KWARGS):
        
    log = Logging(startup=True)   
    main_page_hrefs = get_all_hot_hrefs()   
    log.add_log('links', main_page_hrefs)
    
    print('scraped mainpage')
    
    scrapedPages = ScrapeAllPages(links = main_page_hrefs)
    hsdata = scrapedPages.hotspots
    scrapedPages.init_downloads(vids_dir=vids_dir, quality='best')
    scrapedPages.do_log()
    
    #quality='worst'
        

    D = DFHandler(hs_data = hsdata)                  
    df = D.create_df(formula, **kwargs)
    D.log.add_csv(df)
        
    V = VideoHandler(mp4_names = scrapedPages.mp4_names,
                    dataFrame = df,
                    vids_dir=vids_dir)
                                             
    V.init_cuts()
    V.process_vids()
    V.concat_vids()


    now = datetime.now()   
    t = now.strftime("%m:%d_%H:%M:%S")
    log.add_log('End', t)


def skip_downloads(hspath = HS_PATH,
                vids_dir = VIDSDIR,                
                formula = FORMULA,
                kwargs = KWARGS):
        
    ### loads from logfiles in tests
        
    log = Logging(startup=True)   
    
    V = create_VideoHandler(vids_dir=vids_dir,
                            hspath=hspath,
                            formula=formula,
                            kwargs=kwargs)
                            
    V.init_cuts()
    V.process_vids()
    V.concat_vids()   
    
    now = datetime.now()   
    t = now.strftime("%m:%d_%H:%M:%S")
    log.add_log('End', t)






### helpers
def create_DFHandler(hspath = HS_PATH,
            formula = FORMULA,
            kwargs = KWARGS):
    
    ### create DF from logfile in hspath
    ### used to skip downloads
    
    hsdata = load_hsdata_from_log(hspath)
    
    D = DFHandler(hs_data = hsdata)         
    df = D.create_df(formula, **kwargs)
    return [D, df]

    
def create_VideoHandler(vids_dir = VIDSDIR,
        hspath = HS_PATH,
        formula = FORMULA,
        kwargs = KWARGS):
    ### create VideoHandler from logfile data
    
    mp4_names =  {}

    outputs = create_DFHandler(hspath = hspath,
                                formula = formula,
                                kwargs=kwargs)
    D = outputs[0]
    df = outputs[1]
    
    links = [link for link in D.hs_data.keys()]
    
    scrapedPages = ScrapeAllPages(links = links)
    
    for link in links:
        mp4_names[link] = scrapedPages.get_mp4_name(link)
 
    V = VideoHandler(mp4_names = mp4_names,
                 dataFrame = df,
                 vids_dir = vids_dir)
    

    # V.init_cuts()
    # V.process_vids()
    # V.concat_vids()
    return V
    
    
    
def load_hsdata_from_log(file = r'.\imabust\tests\individual_page_scraper.txt'):
    with open(file, 'r') as f:
        txt = f.read()
    
    r = re.compile('{"hotspots.*')
    rsearch = re.search(r,txt)
    
    hsdata = rsearch.group()
    hsada = json.loads(hsdata)
    hsdata = hsdata['hotspots']
    
    return hsdata
