
from imabust.movie_page_handler import ScrapeAllPages
from imabust.main_page_handler import get_all_hot_hrefs
from imabust.hotspot_calculations  import DFHandler
from imabust.video_handler import VideoHandler
from imabust.ph_logging import Logging
from imabust import main
from imabust import formulas
import json

VIDSDIR = r'.\imabust\vids'
FORMULA = formulas.rolling
KWARGS = {'window': 20,
            'std': 1}
               
outputs = main.run_main(vids_dir = VIDSDIR,
        formula = FORMULA,
        kwargs = KWARGS)
