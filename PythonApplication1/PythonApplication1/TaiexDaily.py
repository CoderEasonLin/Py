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

def insertDB(db, cursor, date, shares, turnover, transaction, taiex, diff):
    sql = "INSERT INTO [dbo].[TaiexDaily]\
                   ([Date]\
                   ,[TradingShares]\
                   ,[TradingTurnover]\
                   ,[Transaction]\
                   ,[Taiex]\
                   ,[Diff])\
             VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (date, shares, turnover, transaction, taiex, diff)
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
    url = "http://www.tse.com.tw/exchangeReport/FMTQIK?response=html&date=" + dateStr
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'lxml')

    for row in soup.select('tr'):
        cols = row.find_all('td')
        try:
            if len(cols) == 6:
                if cols[0].text.strip() != '日期':
                    date = datetime.datetime.strptime('0' + cols[0].text.strip(), '%Y/%m/%d')
                    date = datetime.datetime(date.year + 1911, date.month, date.day)
                    shares = cols[1].text.strip().replace(',', '')
                    turnover = cols[2].text.strip().replace(',', '')
                    transaction = cols[3].text.strip().replace(',', '')
                    taiex = cols[4].text.strip().replace(',', '')
                    diff = cols[5].text.strip().replace(',', '')
                    print(date, shares, turnover, transaction, taiex, diff)
                    insertDB(db, cursor, date.strftime('%Y/%m/%d'), shares, turnover, transaction, taiex, diff)
        except Exception as e:
            print(e)
            logging.error("insert data error → RowData:" + str(row) + ", error msg:" + str(e))
            db.rollback()


if __name__ == '__main__':
    # 20171218 開始區分外資自營商

    # 爬電腦當天的資料
    startDate = None
    nowDate = datetime.datetime.now()

    if startDate is None:
        cursor.execute("SELECT TOP 1 Date FROM [TaiexDaily] ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')

    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[TaiexDaily] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(1)

    db.close()