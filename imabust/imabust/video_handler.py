import subprocess
import pandas as pd
#from datetime import timedelta
from imabust.ph_logging import Logging
from glob import glob
import os
from datetime import datetime

###util for ffmpeg
# import cv2

class VideoHandler:
    def __init__(self, mp4_names, dataFrame, vids_dir=r'.\imabust\vids'):
        self.mp4_names = mp4_names #set in ScrapeAllPages. Could change to set by DF
        self.df = dataFrame
        self.vids_dir = vids_dir
        
        self.sub_commands = []
        self.iterate_dataFrame()        
        self.log = Logging(logfile = 'video_handler.txt', startup=True)
        
    def init_cuts(self):
        ### external command to be used during runtime
        ### cuts full vids in raw_vids dir to timestamp lengths specified in dataFrame
        for i, cut in enumerate(self.sub_commands):
            if i !=0:
                input_name = cut[0]
                time_start = cut[1]
                vid_length = cut[2]
                output_name = cut[3]
                self.cut_video(input_name, time_start, vid_length, output_name)        
       

    def process_vids(self, scale='1920:1080', fps=30):
        ### external command to be used during runtime
        ### sets all videos to same scale and fps
        ### needed step before concating videos
        ###output in processed_vids
        
        glink = self.vids_dir + '\\' + 'cut_vids' + '\\' + '*.mp4'       
        g = glob(glink)        
        for i, vid in enumerate(g):
            basename = os.path.basename(vid)
            outputname = self.vids_dir + '\\' + 'processed_vids' + '\\' + 'processed_' + basename
            cmd = 'ffmpeg -i {0} -vf "scale={1}:force_original_aspect_ratio=decrease,setsar=1:1,fps={2},pad={1}:-1:-1:color=black" {3}'.format(vid, scale, fps, outputname)
            #cmd = 'ffmpeg -hwaccel cuda -i {0} -vf "scale={1}:force_original_aspect_ratio=decrease,setsar=1:1,fps={2},pad={1}:-1:-1:color=black" {3}'.format(vid, scale, fps, outputname)
            #print(cmd)
            self.log.add_log('process_vids', cmd)
            subprocess.run(cmd, text=True)
            
    def concat_vids(self):
        ### external command to be used during runtime
        ### concats all processed videos into a single output file in output_vids.

        now = datetime.now()
        output_name = self.vids_dir +'\\' + 'output_vids' +'\\' + 'output_' + now.strftime("%m_%d_%Y") + '_.mp4'
        
        glink = self.vids_dir + '\\' + 'processed_vids' + '\\' + '*.mp4'         
        g = glob(glink)
        
        ffmpeg = 'ffmpeg'       
        filter_complex = ' -filter_complex "'
        map = ' -map "[v]" -map "[a]" ' + output_name
               
        for i, vid in enumerate(g):
            #print(vid)
            ffmpeg += ' -i {0}'.format(vid)
            filter_complex += '[{0}:v][{0}:a]'.format(i)
            #filter_complex += '-hwaccel cuda' 
        
        filter_complex += 'concat=n={0}:v=1:a=1[v][a]"'.format(len(g))    
               
        cmd = ffmpeg + filter_complex + map
       # print(cmd)
        self.log.add_log('concat_vid', cmd)
        subprocess.run(cmd, text=True)        

    def cut_video(self, input_name, time_start, vid_length, output_name):
        ### helper func for init_cuts
        ### cuts video to hotspot data 
        ### outputs to cut_vids
        
        self.log.add_log('cut_video', ['ffmpeg', '-i', input_name, '-ss', time_start, '-t', vid_length, '-async', '1', output_name])
        subprocess.run(['ffmpeg', '-i', input_name, '-ss', time_start, '-t', vid_length, '-async', '1', output_name])
            
    def iterate_dataFrame(self):
        ### init helper func 
        ### iterates through df and sets timestart and time end to self.sub_commands
        
        consecutive_shot = 1
        #vid_length = 1
        prev_href = self.df.iloc[0,2]
        prev_timestamp = self.df.iloc[0,0]
        vidstart_timestamp = self.df.iloc[0,0]
        
        #new_vid = True
        for index, row in self.df.iterrows():
            
            timestamp = row['timestamps']           
            href = row['href']
        
            if href == prev_href and timestamp == vidstart_timestamp + consecutive_shot:
                consecutive_shot+=1

        
            else:
                
                time_start = vidstart_timestamp * 5
                vid_length = consecutive_shot * 5
                
                input_name = self.vids_dir +'\\'+ 'raw_vids' + '\\' + self.mp4_names[prev_href] + '.mp4' 
                output_name = self.vids_dir +'\\'+ 'cut_vids' +'\\' + self.mp4_names[prev_href] + '_' + str(vidstart_timestamp) + '.mp4'
               
                
                self.sub_commands.append([input_name, str(time_start), str(vid_length), output_name])
                
                vidstart_timestamp = timestamp
                
                prev_href = href
                consecutive_shot=1   
            