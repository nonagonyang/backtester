import csv
from datetime import date,timedelta,datetime


current_date=date.today().isoformat()
yesterday=(date.today()-timedelta(days=1)).isoformat()

#use a csv file containing stocks in QQQ to generate an array of QQQ symbols
qqq_symbols=[]


with open("qqq.csv") as f:
    reader=csv.reader(f) 
    for line in reader:
        #each line the first index is the company name and the second one is the symbol
        qqq_symbols.append(line[1])




logs=[]
runstrats=None