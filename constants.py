import os

LOGFILE_NAME = 'Status.txt'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAXLINE_LEN = 100
LOGFILE_PATH = os.path.join(SCRIPT_DIR, LOGFILE_NAME)
CONFIGFILE_PATH = os.path.join(SCRIPT_DIR, 'Config.zip')
CONFIG_DATA = {'lastdate': '',
               'alldates': []}
FILE_ON_GOGGLE_DRIVE = "StatusTracking1.txt"
CLIENT_SECRETS_JSON = 'client_secrets.json'