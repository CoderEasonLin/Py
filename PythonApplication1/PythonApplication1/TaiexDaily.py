# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import os
import pymssql
import logging
import time
import datetime

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

    db = pymssql.connect(".", "sa", "sa", "StockAnalysis")
    cursor = db.cursor()
    
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
    db.close()


if __name__ == '__main__':
    # 爬一段日期的資料
    startDate = datetime.datetime(2015, 5, 19)
    nowDate = datetime.datetime.now()
    while startDate <= nowDate:
        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(28)


    # 爬電腦當天的資料
    #main(datetime.datetime(2017, 12, 18))