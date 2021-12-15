import pandas as pd



def simple_max_60(self, **kwargs):
    #for link, series in links_in_series.items():
    
    list_ds = kwargs['list_ds']
    n = kwargs['n']
    
    sm60_df = pd.DataFrame([])
    for df in list_ds:
        medi = df['hotspots'].median()
        df['hotspots'] = df['hotspots'].divide(medi)
    
        sm60_df = sm60_df.append(df)
        sm60_df = sm60_df.sort_values(by='hotspots', ascending = False)
        sm60_df = sm60_df.head(n)
        
        sm60_df = sm60_df.sort_values(by='timestamps', ascending = True)
    self.df = sm60_df
    #return sm60_df
    
def moving_average(self, **kwargs):
    list_ds = kwargs['list_ds']
    

def standard_dev(self, **kwargs):
    list_ds = kwargs['list_ds']
    n = kwargs['n']










#######    
def simple_max_60_ds(self, **kwargs):
    df = self.df    
    #ds = ds.divide(ds.median())
    df['hotspots'] = df['hotspots'].divide(df['hotspots'].median())
    return df
    
    
def standard_dev_ds(ds):
    ds = ds.std()
    return ds
    
    

def rolling(self, single_df, **kwargs):
    window = kwargs['window']
    std = kwargs['std']

    roll_mean = single_df['hotspots'].rolling(window).mean()
    roll_std = single_df['hotspots'].rolling(window).std() * std
    
    single_df['hotspots'] = single_df['hotspots'].ge(roll_mean+roll_std)
    
    return single_df
    