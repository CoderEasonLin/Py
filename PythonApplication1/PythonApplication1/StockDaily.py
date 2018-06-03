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
    dateStr = date.strftime("%Y%m%d")
    url = "http://www.tse.com.tw/exchangeReport/MI_INDEX?response=html&date=" + dateStr + "&type=ALLBUT0999"
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'lxml')

    for row in soup.select('tr'):
        cols = row.find_all('td')
        try:
            if len(cols) == 16 and cols[0].text.strip() != '證券代號':
                stockId = cols[0].text.strip()
                tradingShare = parseNumber(cols[2].text)
                transaction = parseNumber(cols[3].text)
                turnover = parseNumber(cols[4].text)
                openPrice = parseNumber(cols[5].text)
                dayHigh = parseNumber(cols[6].text)
                dayLow = parseNumber(cols[7].text)
                closePrice = parseNumber(cols[8].text)
                upDown = cols[9].text.strip()
                upDownValue = parseNumber(cols[10].text)
                if upDown == "-":
                    upDownValue = "-" + upDownValue
                lastBuyPrice = parseNumber(cols[11].text)
                lastBuyCount = parseNumber(cols[12].text)
                lastSellPrice = parseNumber(cols[13].text)
                lastSellCount = parseNumber(cols[14].text)
                per = parseNumber(cols[15].text)

                insertDB(db, cursor, dateStrToDB, stockId, tradingShare, turnover, transaction, openPrice, dayHigh, dayLow, closePrice, upDownValue, lastBuyPrice, lastBuyCount, lastSellPrice, lastSellCount, per)
        except Exception as e:
            print("insert data error → RowData:" + str(row) + ", error msg:" + str(e))
            logging.error("insert data error → RowData:" + str(row) + ", error msg:" + str(e))
            db.rollback()


if __name__ == '__main__':
    # 20171218 開始區分外資自營商

    # 爬電腦當天的資料
    startDate = None
    nowDate = datetime.datetime.now()

    if startDate is None:
        cursor.execute("SELECT TOP 1 Date FROM [StockDaily] ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')

    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[StockDaily] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(1)

    db.close()