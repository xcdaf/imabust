import pandas as pd
import numpy as np
from imabust.ph_logging import Logging
import matplotlib.pyplot as plt

### hotspots {link: [hotspots]}


### output ---> 300s, 60 timestamps
class DFHandler:
    def __init__(self, hs_data, remove_intro=True):
        
        self.hs_data = hs_data ### hotspots {'link1' : [hotspots]....} 
        self.remove_intro = remove_intro
        self.list_df = self.convert_raw_to_list_df() #[df1, df2...]
        self.log = Logging(logfile = 'logdf.csv')
        
        #self.df = self.create_df() moved to external runtime
            
    def convert_raw_to_list_df(self):
        list_df = []
        for link, raw_data in self.hs_data.items():
            ds = pd.Series(raw_data)
            
            if self.remove_intro: #around 1 min
                ds = ds[15:]

            ds = ds.reset_index()
            ds = ds.rename({'index':'timestamps', 0:'hotspots'}, axis='columns')
            ds['href'] = link           
            list_df.append(ds)
            
        return list_df

    def create_df(self, func, **kwargs):
        #for link, series in links_in_series.items():
        df = pd.DataFrame([])
             
        for single_df in self.list_df:           
            single_df = func(self, single_df, **kwargs)       
            df = df.append(single_df)
       
        df = df.loc[df['hotspots'], :]    
        return df
    
    
    
    #### not used for now
    def post_cleanup(self, df, video_n_length=60, sort_hotspots=True, sort_timestamps=True):
        
        if video_n_length:
            df = df.head(video_n_length)
        
        if sort_hotspots:
            df = df.sort_values(by='hotspots', ascending = False)
            
        if sort_timestamps:
            df = df.sort_values(by='timestamps', ascending = True)
        
        return df
                 
    
    def matplot(self, **kwargs): 
        fig, ax = plt.subplots()      
        for name, data in kwargs.items():           
            ax.plot(data, label=name)
            
        plt.show()


    def return_single_series(self, href):
        ds = pd.Series(self.hs_data[href])
        
        if self.remove_intro:
            ds = ds[15:]
        ds = ds.reset_index()
        ds = ds.rename({'index':'timestamps', 0:'hotspots'}, axis='columns')
        ds['href'] = href 
        return ds




if __name__ == '__main__':
    import json
    with open(r'.\txt_files\hotspots_test.txt', 'r') as f:
         
        hs_data = json.loads(f.read())
        D = DFHandler(hs_data)
        
        
        D.list_ds.to_csv('sm60_df2.csv')
        #print(D.df.columns)
        
        #'https://www.pornhub.com/view_video.php?viewkey=ph6159bd5284187'  
        
        # print(D.dict_ds['https://www.pornhub.com/view_video.php?viewkey=ph6159bd5284187'])
        # print(D.dict_ds['https://www.pornhub.com/view_video.php?viewkey=ph6159bd5284187'].columns)
        # D.dict_ds['https://www.pornhub.com/view_video.php?viewkey=ph6159bd5284187'].to_csv('pp.csv')
        #hs_df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in hs_data.items()]))
        
    
        
    
