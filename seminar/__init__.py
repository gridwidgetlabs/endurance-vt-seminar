import os

__version__ = '0.1.0'

def setup():
    os.environ.setdefault('ENDURANCE_SETTINGS_MODULE', 'seminar.settings')