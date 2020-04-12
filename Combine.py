from Plot_AQI import avg_data_2013, avg_data_2014, avg_data_2015, avg_data_2016
import requests
import sys
import pandas as pd
import os
import csv
from bs4 import BeautifulSoup

def met_data(month,year):
    
    file_html = open('/Data/Html_Data/{}/{}.html'.format(year,month),'rb')
    plain_text = file_html.read()
    
    tempD = []
    finalD = []
#Get Tablerows tr data in a list tempD    
    soup=BeautifulSoup(plain_text, "lxml")
    for table in soup.findAll('table', {'class':'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a=tr.get_text()
                tempD.append(a)            
#Get number fo rows. 33 rows                 
    rows=len(tempD)/15
#From tempD format all data into 33 rows in new list finalD    
    for times in range(round(rows)):
        newtempD=[]
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)
        
    length=len(finalD)
    
#Exclude the last row which is not required i.e. Monthly Means data.    
    finalD.pop(length - 1)
#Exclude the headers which will be added later. 
    finalD.pop(0)
#Pop irrelevant columns which are always spaces or nulls or zeros.    
    for a in range(len(finalD)):
        finalD[a].pop(14) #FG Column
        finalD[a].pop(13) #TS Column
        finalD[a].pop(12) #SN Column
        finalD[a].pop(11) #RA Column
        finalD[a].pop(10) #VG Column
        finalD[a].pop(6)  #PP Column
        finalD[a].pop(4)  #SLP Column
        finalD[a].pop(0)  #Day Column
        
    return finalD

# This is the final combine fumction to create one single file including all files.
def data_combine(year, cs):
    for a in pd.read_csv(r'/Data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist

#Main Function to create folder and combine the data from AQI and HTML files.
if __name__ == "__main__":
    if not os.path.exists("/Data/Real-Data"):
        os.makedirs("/Data/Real-Data")
#Create csv file for every year first before combine.
    for year in range(2013, 2017):
        final_data = []
        with open('/Data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1, 13):
            temp = met_data(month, year)
            final_data = final_data + temp
#Get the data i.e. PM2.5 column from AQI files            
        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()

        if len(pm) == 364:
            pm.insert(364, '-')
#Insert that PM2.5 column ot the list at teh end as Dependent value.
        for i in range(len(final_data)-1):
            # final[i].insert(0, i + 1)
            final_data[i].insert(7, pm[i])
#Create CSV file with append mode.
        with open('/Data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
#Below code is just to delete/not to write rows which has valeus as spaces or '-'.
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)
   
     
    total=data_2013+data_2014+data_2015+data_2016
    
    with open('/Data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
df=pd.read_csv(r'/Data/Real-Data/Real_Combine.csv')


