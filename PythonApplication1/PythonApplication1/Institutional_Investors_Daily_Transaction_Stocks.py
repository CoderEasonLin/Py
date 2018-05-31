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

def insertDB(db, cursor, who, stockId, buy, sell, diff, hasBigTransaction, date):
    sql = "INSERT INTO [dbo].[InstitutionalInvestorsDailyTransactionStocks]\
                    ([Date]\
                    ,[StockId]\
                    ,[Who]\
                    ,[Buy]\
                    ,[Sell]\
                    ,[Diff]\
                    ,[HasBigTransaction])\
                VALUES ('%s', '%s', N'%s', '%s', '%s', '%s', %s)" % \
                    (date, stockId, who, buy, sell, diff, hasBigTransaction)
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
    url = "http://www.tse.com.tw/fund/TWT38U?response=html&date=" + dateStr
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'lxml')

    for row in soup.select('tr'):
        cols = row.find_all('td')
        try:
            if len(cols) == 12:
                if cols[1].text.strip() != '證券代號':
                    who = '外資及陸資(不含外資自營商)'
                    stockId = cols[1].text.strip()
                    buy = cols[3].text.strip().replace(',', '')
                    sell = cols[4].text.strip().replace(',', '')
                    diff = cols[5].text.strip().replace(',', '')
                    hasBigTransaction = 1 if cols[5].text.strip() == '*' else 0
                    print(who, stockId, buy, sell, diff, hasBigTransaction)
                    insertDB(db, cursor, who, stockId, buy, sell, diff, hasBigTransaction, dateStrToDB)

                    who = '外資自營商'
                    buy = cols[6].text.strip().replace(',', '')
                    sell = cols[7].text.strip().replace(',', '')
                    diff = cols[8].text.strip().replace(',', '')
                    insertDB(db, cursor, who, stockId, buy, sell, diff, hasBigTransaction, dateStrToDB)

                    who = '外資及陸資'
                    buy = cols[9].text.strip().replace(',', '')
                    sell = cols[10].text.strip().replace(',', '')
                    diff = cols[11].text.strip().replace(',', '')
                    insertDB(db, cursor, who, stockId, buy, sell, diff, hasBigTransaction, dateStrToDB)
            elif len(cols) == 6:
                if cols[1].text.strip() != '證券代號' and cols[1].text.strip() != '':
                    who = '外資及陸資'
                    stockId = cols[1].text.strip()
                    buy = cols[3].text.strip().replace(',', '')
                    sell = cols[4].text.strip().replace(',', '')
                    diff = cols[5].text.strip().replace(',', '')
                    hasBigTransaction = 1 if cols[5].text.strip() == '*' else 0
                    print(who, stockId, buy, sell, diff, hasBigTransaction)
                    insertDB(db, cursor, who, stockId, buy, sell, diff, hasBigTransaction, dateStrToDB)
        except Exception as e:
            print(e)
            logging.error("insert data error → Who:" + who + ", RowData:" + str(row) + ", error msg:" + str(e))
            db.rollback()


if __name__ == '__main__':
    # 20171218 開始區分外資自營商

    # 爬電腦當天的資料
    startDate = None
    nowDate = datetime.datetime.now()

    if startDate is None:
        cursor.execute("SELECT TOP 1 Date FROM InstitutionalInvestorsDailyTransactionStocks ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')

    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[InstitutionalInvestorsDailyTransactionStocks] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(1)

    db.close()