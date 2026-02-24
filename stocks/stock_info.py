import os

from jqdatasdk import *
from dotenv import load_dotenv

load_dotenv()

auth(os.environ['USERNAME'], os.environ['PASSWORD'])

df = get_all_securities(date='2020-10-10')
print(df[:5])