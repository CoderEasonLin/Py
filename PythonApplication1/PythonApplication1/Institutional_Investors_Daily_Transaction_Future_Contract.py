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

def insertDB(db, cursor, date, who, product, long, longTurnover, short, shortTurnover, longShortDiff, longShortDiffTurnover, longTotal, longTotalTurnover, shortTotal, shortTotalTurnover, longShortTotalDiff, longShortTotalDiffTurnover):
    sql = "INSERT INTO [dbo].[FuturesContract]\
           ([Date]\
           ,[ProductName]\
           ,[Who]\
           ,[LongCount]\
           ,[LongTurnover]\
           ,[ShortCount]\
           ,[ShortTurnover]\
           ,[LongShortDiffCount]\
           ,[LongShortDiffTurnover]\
           ,[LongTotalCount]\
           ,[LongTotalTurnover]\
           ,[ShortTotalCount]\
           ,[ShortTotalTurnover]\
           ,[LongShortTotalDiffCount]\
           ,[LongShortTotalDiffTurnover])\
     VALUES ('%s', N'%s', N'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (date, product, who, long, longTurnover, short, shortTurnover, longShortDiff, longShortDiffTurnover, longTotal, longTotalTurnover, shortTotal, shortTotalTurnover, longShortTotalDiff, longShortTotalDiffTurnover)
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
    url = "http://www.taifex.com.tw/chinese/3/7_12_3.asp"
    d = {'goday': '', 'DATA_DATE_Y': date.year, 'DATA_DATE_M': date.month, 'DATA_DATE_D': date.day, 'syear': date.year, 'smonth': date.month, 'sday': date.day, 'datestart': dateStrToDB, 'COMMODITY_ID': ''}
    data = "goday=&DATA_DATE_Y={0}&DATA_DATE_M={1}&DATA_DATE_D={2}&syear={0}&smonth={1}&sday={2}&datestart={3}&COMMODITY_ID=".format(date.year, date.month, date.day, dateStrToDB)
    res = requests.post(url, data=d)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')

    cursor.execute("DELETE FROM [dbo].[FuturesContract] WHERE Date = '%s'" % (dateStrToDB))
    db.commit()

    product = ''
    count = 0
    for row in soup.select('tr'):
        cols = row.find_all('td')
        try:
            if len(cols) == 15:
                count = 1
                product = cols[1].text.strip()
                who = cols[2].text.strip()
                long = cols[3].text.strip().replace(',', '')
                longTurnover = cols[4].text.strip().replace(',', '')
                short = cols[5].text.strip().replace(',', '')
                shortTurnover = cols[6].text.strip().replace(',', '')
                longShortDiff = cols[7].text.strip().replace(',', '')
                longShortDiffTurnover = cols[8].text.strip().replace(',', '')
                longTotal = cols[9].text.strip().replace(',', '')
                longTotalTurnover = cols[10].text.strip().replace(',', '')
                shortTotal = cols[11].text.strip().replace(',', '')
                shortTotalTurnover = cols[12].text.strip().replace(',', '')
                longShortTotalDiff = cols[13].text.strip().replace(',', '')
                longShortTotalDiffTurnover = cols[14].text.strip().replace(',', '')
                insertDB(db, cursor, dateStrToDB, who, product, long, longTurnover, short, shortTurnover, longShortDiff, longShortDiffTurnover, longTotal, longTotalTurnover, shortTotal, shortTotalTurnover, longShortTotalDiff, longShortTotalDiffTurnover)
            elif len(cols) == 13 and count < 3:
                count += 1
                who = cols[0].text.strip()
                long = cols[1].text.strip().replace(',', '')
                longTurnover = cols[2].text.strip().replace(',', '')
                short = cols[3].text.strip().replace(',', '')
                shortTurnover = cols[4].text.strip().replace(',', '')
                longShortDiff = cols[5].text.strip().replace(',', '')
                longShortDiffTurnover = cols[6].text.strip().replace(',', '')
                longTotal = cols[7].text.strip().replace(',', '')
                longTotalTurnover = cols[8].text.strip().replace(',', '')
                shortTotal = cols[9].text.strip().replace(',', '')
                shortTotalTurnover = cols[10].text.strip().replace(',', '')
                longShortTotalDiff = cols[11].text.strip().replace(',', '')
                longShortTotalDiffTurnover = cols[12].text.strip().replace(',', '')
                insertDB(db, cursor, dateStrToDB, who, product, long, longTurnover, short, shortTurnover, longShortDiff, longShortDiffTurnover, longTotal, longTotalTurnover, shortTotal, shortTotalTurnover, longShortTotalDiff, longShortTotalDiffTurnover)

        except Exception as e:
            print(e)
            logging.error("insert data error → Who:" + who + ", RowData:" + str(row) + ", error msg:" + str(e))
            db.rollback()
    


if __name__ == '__main__':
    # 20171218 開始區分外資自營商

    # 爬電腦當天的資料，並補上之前缺的資料
    #startDate = datetime.datetime(2017, 12, 18)
    startDate = None
    nowDate = datetime.datetime.now()

    if startDate is None:
        cursor.execute("SELECT TOP 1 Date FROM FuturesContract ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else row[0]
    while startDate <= nowDate:
        print(startDate)
        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(1)

    db.close()