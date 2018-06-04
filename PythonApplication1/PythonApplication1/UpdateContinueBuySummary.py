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

def parseNumber(s):
    try:
        result = s.strip().replace(',', '')
        test = float(result)
        return result
    except Exception as e:
        print(e)
        return "0"


def insertDB(db, cursor, date, stockId, tradingShare, turnover, transaction, openPrice, dayHigh, dayLow, closePrice, upDown, lastBuyPrice, lastBuyCount, lastSellPrice, lastSellCount, per):
    sql = "INSERT INTO [dbo].[StockDaily]\
                   ([Date]\
                   ,[StockId]\
                   ,[TradingShare]\
                   ,[Transaction]\
                   ,[Turnover]\
                   ,[OpenPrice]\
                   ,[DayHigh]\
                   ,[DayLow]\
                   ,[ClosePrice]\
                   ,[UpDown]\
                   ,[LastBuyPrice]\
                   ,[LastBuyCount]\
                   ,[LastSellPrice]\
                   ,[LastSellCount]\
                   ,[PER])\
             VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (date, stockId, tradingShare, transaction, turnover, openPrice, dayHigh, dayLow, closePrice, upDown, lastBuyPrice, lastBuyCount, lastSellPrice, lastSellCount, per)
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
    try:
        cursor.execute("EXECUTE [dbo].[InsertContinueBuySummary] N'外資' ,'%s'" % dateStrToDB)
        db.commit()

        cursor.execute("EXECUTE [dbo].[InsertContinueBuySummary] N'投信' ,'%s'" % dateStrToDB)
        db.commit()
        
        cursor.execute("EXECUTE [dbo].[InsertContinueBuySummary] N'自營商' ,'%s'" % dateStrToDB)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

if __name__ == '__main__':
    # 爬電腦當天的資料
    startDate = None
    nowDate = datetime.datetime.now()

    if startDate is None:
        cursor.execute("SELECT TOP 1 Date FROM [ContinueBuySummary] ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')

    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[ContinueBuySummary] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        startDate = startDate + datetime.timedelta(1)

    db.close()