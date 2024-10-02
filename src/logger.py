#helps to detect the error with datetime and person's name

import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"    #specifies the date and time

logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE) #by using this all the log file will be stored in 'logs' specified folder

os.makedirs(logs_path, exist_ok=True)   #if not exists then it will create

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)   

logging.basicConfig(    #basic configuration of log file
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)