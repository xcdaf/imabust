
from imabust.movie_page_handler import ScrapeAllPages
from imabust.main_page_handler import get_all_hot_hrefs
from imabust.hotspot_calculations  import DFHandler
from imabust.video_handler import VideoHandler
from imabust.ph_logging import Logging
from imabust import formulas
from datetime import datetime
import json


#Settings ###############################
# l = 'https://www.pornhub.com/view_video.php?viewkey='
# VIDSDIR = r'.\imabust\vids'

# FORMULA = formulas.rolling
# KWARGS = {'window': 20,
            # 'std': 1}

# HS_PATH = r'.\imabust\tests\test_files\hotspots.txt'
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
                    vid_dir=vids_dir)
                                             
    V.init_cuts()
    V.process_vids()
    V.concat_vids()


    now = datetime.now()   
    t = now.strftime("%m:%d_%H:%M:%S")
    log.add_log('End', t)

def only_DFHandler(formula = FORMULA,
            kwargs = KWARGS,
            hs_path= HS_PATH,
            href = PH_LINK):

        
    with open(hs_path, 'r') as f:
        hsdata = f.read()
        hsdata = hsdata.replace("'", '"')
        hsdata = json.loads(hsdata)
        
    D = DFHandler(hs_data = hsdata)
    #kwargs['list_ds'] = D.list_ds              
    df = D.create_df(formula, **kwargs)
    
    #ds = D.return_single_series(href=href) 
    #ds.to_csv('ph61658be992234.csv')
    #new_ds = formulas.rolling(ds)
    
    # plot_kwargs = {'df' : df#,
                    # # #'new_ds' : new_ds
                    # }
    
    #D.matplot(**plot_kwargs)
    #print(ds.shape)
    
    return [D, df]
    #return [D,df]
    #return [ds, new_ds]
    
    
def test_VideoHandler(vids_dir = VIDSDIR):
    mp4_names =  {}

    outputs = only_DFHandler()
    D = outputs[0]
    df = outputs[1]
    
    links = [link for link in D.hs_data.keys()]
    
    scrapedPages = ScrapeAllPages(links = links)
    
    for link in links:
        mp4_names[link] = scrapedPages.get_mp4_name(link)
    


    V = VideoHandler(mp4_names = mp4_names,
                 dataFrame = df,
                 vids_dir = vids_dir)
    

    V.init_cuts()
    #V.process_vids()
    #V.concat_vids()
    return V