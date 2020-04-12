import os
import time
import requests
import sys

def retrieve_html():
    for year in range(2013,2019):
        for month in range(1,13):
            if month < 10:
                url='https://en.tutiempo.net/climate/0{}-{}/ws-432950.html'.format(month,year)
            else:
                url='https://en.tutiempo.net/climate/{}-{}/ws-432950.html'.format(month,year)
            texts=requests.get(url)
            text_utf=texts.text.encode('utf=8')
        
            if not os.path.exists("/Data/Html_Data/{}".format(year)):
                os.makedirs("/Data/Html_Data/{}".format(year))
            with open("/Data/Html_Data/{}/{}.html".format(year,month),'wb') as output:
                output.write(text_utf)
#When ever we execute print statements output will be written to buffer. 
#And we will see the output on screen when buffer get flushed(cleared). 
#By default buffer will be flushed when program exits. 
#BUT WE CAN ALSO FLUSH THE BUFFER MANUALLY by using "sys.stdout.flush()" statement in the program       
            sys.stdout.flush()   #Basically flush everything that is created in the file.
        
if __name__ =="__main__":
    start_time=time.time()
    retrieve_html()
    stop_time=time.time()
    print("Time taken is {}".format(stop_time-start_time))
    