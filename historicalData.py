import requests
import csv
import datetime
import time
import os
import re
from selenium import webdriver
import numpy as np
import pandas as pd
import mpl_finance as mpl
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import talib
#NOTICE: Check newest FR
#NOTICE: bin->1h, fixed or dynamic?

class historicalData():
    dayOfMonthNotYear = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dayOfMonthYear = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    fundingRateHistory = {}
    bin1mHistory = []
    recorded = []

    def requestJSON(self,url):
        #print(requests.get(url).text)
        #print(requests.get(url).json())
        return requests.get(url).json()

    def requestNewestFR(self,url="https://www.bitmex.com/app/contract/XBTUSD"):
        driver = webdriver.Chrome('./chromedriver')
        driver.maximize_window()
        driver.get(url)
        newestFR = re.findall(r"<td class=\"gridCell\"><span class=\"tooltipWrapper\">Funding Rate</span></td><td class=\"gridCell\">(.+?)%",driver.page_source)
        return(float(newestFR[0]))

    def getFundingRate(self,timestamp):
        timestamp_datetime = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:00.000Z')
        hour = timestamp_datetime.hour
        minute = timestamp_datetime.minute
        seconds = timestamp_datetime.second
        microsecond = timestamp_datetime.microsecond

        secondsOfDay = hour * 3600 + minute * 60 + seconds + microsecond / 1000000
        #Get Funding Rate
        if secondsOfDay <= 43200 and secondsOfDay > 14400:
            tmpStr = 'T12:00:00.000Z'
        # p.m.12:00 to p.m. 20:00
        elif secondsOfDay <= 72000 and secondsOfDay > 43200:
            tmpStr = 'T20:00:00.000Z'
        # a.m.00:00 to a.m. 04:00
        elif secondsOfDay <= 14400:
            tmpStr = 'T04:00:00.000Z'
        # p.m.20:00 to a.m. 00:00
        elif secondsOfDay>72000:
            #datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:00.000Z')
            tmpStr = 'T04:00:00.000Z'
            timestamp = datetime.datetime.strptime(str(timestamp)[:10], '%Y-%m-%d')+ datetime.timedelta(days=1)
        else:
            print("Get funding rate error!")

        timeFR = str(timestamp)[:10]+tmpStr
        return historicalData.fundingRateHistory[timeFR]

    def writeFile(self,filename):
        with open(filename, 'a', newline='') as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile)
            length = len(historicalData.bin1mHistory)
            for i in range(0, length):
                writer.writerow(historicalData.bin1mHistory[i])

    def isYear(self,year):
        if year%4 == 0 & year%100 != 0:
            return True
        elif year%400 == 0:
            return True
        else:
            return False

    def crawlFR(self):
        # Earlist:2016-05-14T12:00:00.000Z
        print("Start to crawl funding rate history....")
        i = 0
        go = True
        while(go):
            print("Crawling funding rate("+str(i+1)+")...")
            url = "https://www.bitmex.com/api/v1/funding?count=500&start="+str(500*i)+"&reverse=true&filter=%7B%22symbol%22%3A%22XBTUSD%22%7D"
            fundingRate = self.requestJSON(url)
            for index in range(0, len(fundingRate)):
                historicalData.fundingRateHistory[fundingRate[index]['timestamp']] = fundingRate[index]['fundingRate']*100
                if (fundingRate[index]['timestamp'] == '2016-05-14T12:00:00.000Z'):
                    go = False
                    break
            i += 1
        #Get newest funding rate
        utcNow = datetime.datetime.utcnow()
        hour = utcNow.hour
        minute = utcNow.minute
        seconds = utcNow.second
        microsecond = utcNow.microsecond
        secondsOfDay = hour * 3600 + minute * 60 + seconds + microsecond / 1000000
        # Get Funding Rate
        #a.m.04:00 to p.m. 12:00
        if secondsOfDay <= 43200 and secondsOfDay > 14400:
            tmpStr = 'T12:00:00.000Z'
        # p.m.12:00 to p.m. 20:00
        elif secondsOfDay <= 72000 and secondsOfDay > 43200:
            tmpStr = 'T20:00:00.000Z'
        # a.m.00:00 to a.m. 04:00
        elif secondsOfDay <= 14400:
            tmpStr = 'T04:00:00.000Z'
        # p.m.20:00 to a.m. 00:00
        elif secondsOfDay>72000:
            #datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:00.000Z')
            tmpStr = 'T04:00:00.000Z'
            utcNow = datetime.datetime.strptime(str(utcNow)[:10], '%Y-%m-%d')+ datetime.timedelta(days=1)
        else:
            print("Get funding rate error!")
        timeFR = str(utcNow)[:10] + tmpStr
        newestFR = self.requestNewestFR()

        historicalData.fundingRateHistory[timeFR] = newestFR
        print("The newest FR of", timeFR ," is:",newestFR,"%,please check it in advance")

    def crawlAll(self,filename="BTC.csv",sleep=0,fromYear=2017,fromMonth=1,fromDay=1):
        self.crawlFR()
        historicalData.bin1mHistory = []
        historicalData.recorded = []
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, 'w', newline='') as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'trades', 'volume', 'vwap', 'lastSize', 'turnover','homeNotional', 'foreignNotional','fundingRate'])
        for year in range(fromYear, 2020):
            startMonth = fromMonth if year==fromYear else 1
            dayOfMonth = historicalData.dayOfMonthYear if self.isYear(year) else historicalData.dayOfMonthNotYear
            for month in range(startMonth, 13):
                startDay = fromDay if (year==fromYear and month==fromMonth) else 1
                for day in range(startDay, dayOfMonth[month - 1] + 1):
                    for hour in range(0, 2):
                        hour = str(hour * 12).zfill(2)
                        month = str(month).zfill(2)
                        timestamp = "%d-%s-%dT%s:00:00.000Z" % (year, month, day, hour)
                        timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:00.000Z')
                        if (datetime.datetime.utcnow() - timestamp).total_seconds() < 60:
                            # print("Time is over!")
                            break
                        else:
                            url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=720&reverse=false&startTime=" + str(
                                timestamp)
                            while True:
                                time.sleep(sleep)
                                result = self.requestJSON(url)
                                #print(result[0])
                                if len(result)>0 and result[0]['timestamp']!='':
                                    for i in range(0, len(result)):
                                        if (result[i]['timestamp'] not in historicalData.recorded[-720:]):
                                            fundingRate = self.getFundingRate(result[i]['timestamp'])
                                            historicalData.bin1mHistory.append(list(result[i].values())+[float(fundingRate)])
                                            historicalData.recorded.append(result[i]['timestamp'])
                                        else:
                                            print("Error:" + result[i]['timestamp'] + " Already recorded!")
                                    print(datetime.datetime.now(),"Crawling "+str(timestamp) + ".... Total: " + str(len(result)) + " data")
                                    break
                                else:
                                    print("Request ",str(timestamp)," Error! .... Total: " , str(len(result)) , " data")
        self.writeFile(filename)

    def genFeature(self,input,output):
        print("Start to Generate Feature from",input,"to",output,"......")
        type = ["1min_","5min_","15min_","30min_", "1hr_" , "2hrs_" , "4hrs_" , "12hrs_" ,"1d_"]
        kLine = ['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'trades', 'volume', 'vwap', 'lastSize', 'turnover', 'homeNotional', 'foreignNotional']
        if os.path.exists(output):
            os.remove(output)
        #Write header into file
        with open(output, 'w', newline='') as csvfile:
            header = []
            for i in range(0,len(type)):
                header += [type[i] + element  for element in kLine]
            writer = csv.writer(csvfile)
            writer.writerow(header+['fundingRate'])
        #Read and process data
        rawData = pd.read_csv(input)
        rawData['timestamp'] = pd.to_datetime(rawData['timestamp'])
        #rawData.index = rawData['timestamp']

        #Loop for each type
        print([rawData.loc(str(timestamp)) for timestamp in rawData['timestamp']])

    def getOHLC(self,data,time):

        print("Generating OHLC")

    def plot(self,filename):
        rawData = pd.read_csv(filename)
        rawData['timestamp'] = pd.to_datetime(rawData['timestamp'])
        rawData.index = rawData['timestamp']
        rawData['volume'].plot()
        (rawData['vwap']*4500).plot(color="red")
        plt.show()

if __name__=='__main__':
    #TODO: VWAP=NA?
    history = historicalData()
    #history.plot("BTC2.csv")
    history.genFeature("BTC2.csv","BTC3.csv")