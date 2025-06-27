from jqdatasdk import *
auth('13141244283','Xayida661108*')

df = get_all_securities(date='2020-10-10')
print(df[:5])