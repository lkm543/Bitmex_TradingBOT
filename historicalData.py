import requests
import csv
import datetime
import time
import os
import re
from selenium import webdriver
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
#import talib
#NOTICE: Check newest FR
#TODO: Error in newest FR
#NOTICE: bin->1h, fixed or dynamic?


class historicalData():
    dayOfMonthNotYear = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dayOfMonthYear = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    fundingRateHistory = {}
    bin1mHistory = []
    recorded = []

    def requestJSON(self,url):
        return requests.get(url).json()

    def requestNewestFR(self,url="https://www.bitmex.com/app/contract/XBTUSD"):
        if self.coin=="ETH":
            url = "https://www.bitmex.com/app/contract/ETHUSD"
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
            tmpStr = 'T04:00:00.000Z'
            timestamp = datetime.datetime.strptime(str(timestamp)[:10], '%Y-%m-%d')+ datetime.timedelta(days=1)
        else:
            print("Get funding rate error!")

        timeFR = str(timestamp)[:10]+tmpStr
        return historicalData.fundingRateHistory[timeFR]

    def writeFile(self,filename):
        with open(filename, 'a', newline='') as csvfile:
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

            if self.coin == "BTC":
                url = "https://www.bitmex.com/api/v1/funding?count=500&start="+str(500*i)+"&reverse=true&filter=%7B%22symbol%22%3A%22XBTUSD%22%7D"
            elif self.coin == "ETH":
                url = "https://www.bitmex.com/api/v1/funding?count=500&start="+str(500*i)+"&reverse=true&filter=%7B%22symbol%22%3A%22ETHUSD%22%7D"

            fundingRate = self.requestJSON(url)
            for index in range(0, len(fundingRate)):
                historicalData.fundingRateHistory[fundingRate[index]['timestamp']] = fundingRate[index]['fundingRate']*100
                if (fundingRate[index]['timestamp'] == '2016-05-14T12:00:00.000Z' and self.coin=="BTC"):
                    go = False
                    break
                if (fundingRate[index]['timestamp'] == '2018-08-02T12:00:00.000Z' and self.coin=="ETH"):
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
            tmpStr = 'T04:00:00.000Z'
            utcNow = datetime.datetime.strptime(str(utcNow)[:10], '%Y-%m-%d')+ datetime.timedelta(days=1)
        else:
            print("Get funding rate error!")
        timeFR = str(utcNow)[:10] + tmpStr
        newestFR = self.requestNewestFR()

        historicalData.fundingRateHistory[timeFR] = newestFR
        print("The newest FR of", timeFR ," is:",newestFR,"%,please check it in advance")

    def crawlAll(self,Coin = "BTC",filename="BTC.csv",sleep=0.5,fromYear=2017,fromMonth=1,fromDay=1):
        self.coin = Coin
        if Coin == "ETH":
            fromYear = 2018
            fromMonth = 8
            fromDay = 3
        self.crawlFR()
        print("Median of FR:",np.median(list(self.fundingRateHistory.values())))
        historicalData.bin1mHistory = []
        historicalData.recorded = []
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, 'w', newline='') as csvfile:
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
                            break
                        else:

                            if self.coin == "BTC":
                                url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=720&reverse=false&startTime=" + str(
                                timestamp)
                            elif self.coin == "ETH":
                                url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=ETHUSD&count=720&reverse=false&startTime=" + str(
                                timestamp)
                            while True:
                                time.sleep(sleep)
                                result = self.requestJSON(url)
                                if len(result)>0 and result[0]['timestamp']!='':
                                    for i in range(0, len(result)):
                                        if (result[i]['timestamp'] not in historicalData.recorded[-720:]):
                                            fundingRate = self.getFundingRate(result[i]['timestamp'])
                                            historicalData.bin1mHistory.append(list(result[i].values())+[float(fundingRate)])
                                            historicalData.recorded.append(result[i]['timestamp'])
                                        #else:
                                        #    print("Error:" + result[i]['timestamp'] + " Already recorded!")
                                    print(datetime.datetime.now(),"Crawling "+str(timestamp) + ".... Total: " + str(len(result)) + " data")
                                    break
                                else:
                                    print("Request ",str(timestamp)," Error! .... Total: " , str(len(result)) , " data")
        self.writeFile(filename)

    def complement(self,Coin = "BTC",filename="BTC.csv",sleep=0.5):
        self.coin = Coin
        df = pd.read_csv(filename,header=0)
        lastTimeStamp = df.iloc[-1,0]
        lastDateTime = datetime.datetime.strptime(lastTimeStamp, "%Y-%m-%dT%H:%M:%S.000Z")
        fromYear = lastDateTime.year
        fromMonth = lastDateTime.month
        fromDay = lastDateTime.day

        print("Crawling from", lastTimeStamp)

        historicalData.recorded = list(df.timestamp)
        historicalData.bin1mHistory = []
        self.crawlFR()

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
                            break
                        else:

                            if self.coin == "BTC":
                                url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=720&reverse=false&startTime=" + str(
                                timestamp)
                            elif self.coin == "ETH":
                                url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=ETHUSD&count=720&reverse=false&startTime=" + str(
                                timestamp)
                            while True:
                                time.sleep(sleep)
                                result = self.requestJSON(url)
                                if len(result)>0 and result[0]['timestamp']!='':
                                    for i in range(0, len(result)):
                                        if (result[i]['timestamp'] not in historicalData.recorded[-7200:]):
                                            fundingRate = self.getFundingRate(result[i]['timestamp'])
                                            historicalData.bin1mHistory.append(list(result[i].values())+[float(fundingRate)])
                                            historicalData.recorded.append(result[i]['timestamp'])
                                        #else:
                                        #    print(result[i]['timestamp'] + " Already recorded!")
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

        #Loop for each type
        print([rawData.loc(str(timestamp)) for timestamp in rawData['timestamp']])

    def getOHLC(self,data,time):
        print("Generating OHLC......")

    def analysis(self,filename):
        #toDo everday? varied with time?
        self.rawData = pd.read_csv(filename,header=0)
        for i in range(0,365*1+150):
            upDown = 0
            upUp = 0
            downUP = 0
            downDown = 0
            #len(self.rawData)
            for j in range(i*1440+1,(i+1)*1440):
                lastOpen = self.rawData.loc[j-1, 'open']
                lastClose = self.rawData.loc[j-1, 'close']
                open = self.rawData.loc[j, 'open']
                close = self.rawData.loc[j, 'close']
                if lastOpen < lastClose and open > close:
                    upDown += 1
                elif lastOpen < lastClose and open < close:
                    upUp += 1
                elif lastOpen > lastClose and open < close:
                    downUP += 1
                elif lastOpen > lastClose and open > close:
                    downDown += 1
            print("upDown:",round(upDown/(upDown+upUp)*100,2),"upUp:",round(upUp/(upDown+upUp)*100,2),"downUP:",round(downUP/(downUP+downDown)*100,2),"downDown:",round(downDown/(downUP+downDown)*100,2))


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
    #history.crawlAll("ETH","ETH.csv")
    history.complement("BTC","BTC.csv")
    history.complement("ETH","ETH.csv")
    #history.analysis("ETH.csv")
    #history.analysis("BTC.csv")
