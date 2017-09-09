import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASE_DIR = os.path.join(BASE_DIR, 'cases')
FILE_DIR = os.path.join(BASE_DIR, 'files')
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# QUICKSTART FUNCTION
QUICKSTART_VERSION = '34'
QUICKSTART_BUSCOUNT = 120000
QUICKSTART_LOAD_CASE = True
QUICKSTART_INITIALIZE_PSSE = True
QUICKSTART_CASE = r"""C:\Program Files (x86)\PTI\PSSE34\EXAMPLE\ieee_25bus.sav"""

# PSSE
PSSBIN = r"""C:\Program Files (x86)\PTI\PSSE34\PSSBIN"""

# LOGGING
USE_LOGGING_SETTINGS = False

AUTOMATICALLY_LOG_API_ERRORS = False

ALERT_OUTPUT_DEVICE = 'file_output'
PROGRESS_OUTPUT_DEVICE = 'no_output'
REPORT_OUTPUT_DEVICE = 'file_output'
PROMPT_OUTPUT_DEVICE = 'standard_output'

ALERT_LOG_FILE = os.path.join(LOG_DIR, 'alert.txt')
PROGRESS_LOG_FILE = os.path.join(LOG_DIR, 'progress.txt')
REPORT_LOG_FILE = os.path.join(LOG_DIR, 'report.txt')
PROMPT_LOG_FILE = os.path.join(LOG_DIR, 'prompt.txt')

DATASYNC_CONTROLLER_INTERNAL_LOG_SIZE = 10