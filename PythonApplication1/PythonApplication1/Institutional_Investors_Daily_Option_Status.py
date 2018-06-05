# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import os
import pymssql
import logging
import time
import datetime

db = pymssql.connect(".", "sa", "sa", "StockAnalysis")
cursor = db.cursor()

def insertDb(dateStrToDB, product, option, who, buy, buyTurnover, sell, sellTurnover, diff, diffTurnover, buyTotal, buyTotalTurnover, sellTotal, sellTotalTurnover, diffTotal, diffTotalTurnover):
    sql = "INSERT INTO [dbo].[InstitutionalInvestorsDailyOptionSummary]\
           ([Date]\
           ,[ProductName]\
           ,[Option]\
           ,[Who]\
           ,[Buy]\
           ,[BuyTurnover]\
           ,[Sell]\
           ,[SellTurnover]\
           ,[Diff]\
           ,[DiffTurnover]\
           ,[BuyTotal]\
           ,[BuyTotalTurnover]\
           ,[SellTotal]\
           ,[SellTotalTurnover]\
           ,[DiffTotal]\
           ,[DiffTotalTurnover])\
     VALUES ('%s', N'%s', N'%s', N'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (dateStrToDB, product, option, who, buy, buyTurnover, sell, sellTurnover, diff, diffTurnover, buyTotal, buyTotalTurnover, sellTotal, sellTotalTurnover, diffTotal, diffTotalTurnover)
    cursor.execute(sql)
    db.commit()


def main(date=time.localtime()):
    if not os.path.isdir('log'):
        os.makedirs('log')
    logging.basicConfig(filename='log/getlist-error.log',
                        level=logging.ERROR,
                        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    dateStrToDB = date.strftime("%Y/%m/%d")

    d = {
        'goday': '', 
        'DATA_DATE_Y': date.year, 
        'DATA_DATE_M': date.month, 
        'DATA_DATE_D': date.day, 
        'syear': date.year, 
        'smonth': date.month, 
        'sday': date.day, 
        'datestart': dateStrToDB, 
        'COMMODITY_ID': 'TXO'
    }

    url = "http://www.taifex.com.tw/chinese/3/7_12_5.asp"
    res = requests.post(url, data=d)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')

    product = ''
    option = ''
    for row in soup.select('tr'):
        cols = row.find_all('td')
        try:
            if len(cols) == 16:
                product = cols[1].text.strip()
                option = cols[2].text.strip()

                who = cols[3].text.strip()
                buy = cols[4].text.strip().replace(',', '')
                buyTurnover = cols[5].text.strip().replace(',', '')
                sell = cols[6].text.strip().replace(',', '')
                sellTurnover = cols[7].text.strip().replace(',', '')
                diff = cols[8].text.strip().replace(',', '')
                diffTurnover = cols[9].text.strip().replace(',', '')
                
                buyTotal = cols[10].text.strip().replace(',', '')
                buyTotalTurnover = cols[11].text.strip().replace(',', '')
                sellTotal = cols[12].text.strip().replace(',', '')
                sellTotalTurnover = cols[13].text.strip().replace(',', '')
                diffTotal = cols[14].text.strip().replace(',', '')
                diffTotalTurnover = cols[15].text.strip().replace(',', '')
                insertDb(dateStrToDB, product, option, who, buy, buyTurnover, sell, sellTurnover, diff, diffTurnover, buyTotal, buyTotalTurnover, sellTotal, sellTotalTurnover, diffTotal, diffTotalTurnover)

            elif len(cols) == 14:
                option = cols[0].text.strip()

                who = cols[1].text.strip()
                buy = cols[2].text.strip().replace(',', '')
                buyTurnover = cols[3].text.strip().replace(',', '')
                sell = cols[4].text.strip().replace(',', '')
                sellTurnover = cols[5].text.strip().replace(',', '')
                diff = cols[6].text.strip().replace(',', '')
                diffTurnover = cols[7].text.strip().replace(',', '')
                
                buyTotal = cols[8].text.strip().replace(',', '')
                buyTotalTurnover = cols[9].text.strip().replace(',', '')
                sellTotal = cols[10].text.strip().replace(',', '')
                sellTotalTurnover = cols[11].text.strip().replace(',', '')
                diffTotal = cols[12].text.strip().replace(',', '')
                diffTotalTurnover = cols[13].text.strip().replace(',', '')
                insertDb(dateStrToDB, product, option, who, buy, buyTurnover, sell, sellTurnover, diff, diffTurnover, buyTotal, buyTotalTurnover, sellTotal, sellTotalTurnover, diffTotal, diffTotalTurnover)

            elif len(cols) == 13:
                who = cols[0].text.strip()
                buy = cols[1].text.strip().replace(',', '')
                buyTurnover = cols[2].text.strip().replace(',', '')
                sell = cols[3].text.strip().replace(',', '')
                sellTurnover = cols[4].text.strip().replace(',', '')
                diff = cols[5].text.strip().replace(',', '')
                diffTurnover = cols[6].text.strip().replace(',', '')
                
                buyTotal = cols[7].text.strip().replace(',', '')
                buyTotalTurnover = cols[8].text.strip().replace(',', '')
                sellTotal = cols[9].text.strip().replace(',', '')
                sellTotalTurnover = cols[10].text.strip().replace(',', '')
                diffTotal = cols[11].text.strip().replace(',', '')
                diffTotalTurnover = cols[12].text.strip().replace(',', '')
                insertDb(dateStrToDB, product, option, who, buy, buyTurnover, sell, sellTurnover, diff, diffTurnover, buyTotal, buyTotalTurnover, sellTotal, sellTotalTurnover, diffTotal, diffTotalTurnover)
        
        except Exception as e:
            print("insert data error → RowData:" + str(row) + ", error msg:" + str(e))
            db.rollback()


if __name__ == '__main__':
    # 20171218 開始區分外資自營商
    # 爬電腦當天的資料，並補上之前缺的資料
    #startDate = datetime.datetime(2015, 5, 19)
    startDate = None
    nowDate = datetime.datetime.now()

    if startDate is None:
        cursor.execute("SELECT TOP 1 Date FROM InstitutionalInvestorsDailyOptionSummary ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')
    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[InstitutionalInvestorsDailyOptionSummary] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(1)

    db.close()