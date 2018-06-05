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

def insertDB(db, cursor, date, product, deadline, buyTop5, buyTop10, sellTop5, sellTop10, total):
    sql = "INSERT INTO [dbo].[BigInvestorsFutureContract]\
           ([Date]\
           ,[ProductName]\
           ,[Deadline]\
           ,[BuyTop5]\
           ,[BuyTop10]\
           ,[SellTop5]\
           ,[SellTop10]\
           ,[Total])\
     VALUES ('%s', N'%s', N'%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (date, product, deadline, buyTop5, buyTop10, sellTop5, sellTop10, total)
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
    d = {
            'pFlag': '',
            'yytemp': date.year,
            'mmtemp': date.month,
            'ddtemp': date.day,
            'chooseitemtemp': 'ALL',
            'goday': '',
            'choose_yy': date.year,
            'choose_mm': date.month,
            'choose_dd': date.day,
            'datestart': dateStrToDB,
            'choose_item': 'TX' 
    }
    data = "pFlag=&yytemp={0}&mmtemp={1}&ddtemp={2}&chooseitemtemp=ALL&goday=&choose_yy={0}&choose_mm={1}&choose_dd={2}&datestart={3}&choose_item=TX".format(date.year, date.month, date.day, dateStrToDB)
    url = "http://www.taifex.com.tw/chinese/3/7_8.asp"
    res = requests.post(url, data=d)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')

    product = ''
    for row in soup.select('tr'):
        cols = row.find_all('td')
        try:
            if len(cols) == 11:
                product = cols[0].text.strip()
            elif len(cols) == 10:
                deadline = cols[0].text.strip().replace('\r\n', '').replace('\t', '')
                pattern = re.compile('(\d+)\s*\((\d+)\)')
                split = re.split(pattern, cols[1].text.strip().replace(',', ''))
                buyTop5 = split[1]
                split = re.split(pattern, cols[3].text.strip().replace(',', ''))
                buyTop10 = split[1]
                split = re.split(pattern, cols[5].text.strip().replace(',', ''))
                sellTop5 = split[1]
                split = re.split(pattern, cols[7].text.strip().replace(',', ''))
                sellTop10 = split[1]
                total = cols[9].text.strip().replace(',', '')
                insertDB(db, cursor, dateStrToDB, product, deadline, buyTop5, buyTop10, sellTop5, sellTop10, total)

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
        cursor.execute("SELECT TOP 1 Date FROM BigInvestorsFutureContract ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')
    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[BigInvestorsFutureContract] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(1)

    db.close()