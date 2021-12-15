import pandas as pd
import json
from datetime import datetime

class Logging:
    def __init__(self, logfile='logfile.txt', startup=False):
        
        log_dir = r'.\logging'
        self.logfile = log_dir + '\\' + logfile
        
        self.log_csv = log_dir + '\\' + 'logdf.csv'
        self.log_error = log_dir + '\\' + 'logerror.txt'
        
        if startup:
            self.on_start()
        
    def add_log(self, name, data):
        
        log = {}
        data = str(data)
        log[name] = data

        with open(self.logfile, 'a') as f:
            f.write('\n' +json.dumps(log))

    
    def add_csv(self, df):
        df.to_csv(self.log_csv)
        
    
    def add_error(self, e):
        error = str(e)
        
        with open(self.log_error, 'a') as f:
            f.write('\n' + error)
 
    def on_start(self):      
        now = datetime.now()
                
        t = now.strftime("%m:%d_%H:%M:%S")
        with open(self.logfile, 'w') as f:
            f.write(t)
            
        
        
            