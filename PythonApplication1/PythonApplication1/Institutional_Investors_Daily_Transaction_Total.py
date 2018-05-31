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

def main(date=time.localtime()):
    if not os.path.isdir('log'):
        os.makedirs('log')
    logging.basicConfig(filename='log/getlist-error.log',
                        level=logging.ERROR,
                        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')
    
    dateStrToDB = date.strftime("%Y/%m/%d")
    dateStr = date.strftime("%Y%m%d")
    url = "http://www.tse.com.tw/fund/BFI82U?response=html&dayDate=" + dateStr + "&type=day"
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'lxml')

    for row in soup.select('tr'):
        cols = row.find_all('td')
        if len(cols) == 4:
            if cols[0].text.strip() != '單位名稱' and cols[0].text.strip() != '合計':
                who = cols[0].text.strip()
                buy = cols[1].text.strip().replace(',', '')
                sell = cols[2].text.strip().replace(',', '')
                diff = cols[3].text.strip().replace(',', '')
                print(who, buy, sell, diff)

                try:
                    sql = "INSERT INTO [dbo].[InstitutionalInvestorsDailyTransactionTotal]\
                                    ([Date]\
                                    ,[Who]\
                                    ,[Buy]\
                                    ,[Sell]\
                                    ,[Diff])\
                                VALUES ('%s', N'%s', '%s', '%s', '%s')" % \
                                    (dateStrToDB, who, buy, sell, diff)
                    cursor.execute(sql)
                    db.commit()
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
        cursor.execute("SELECT TOP 1 Date FROM [InstitutionalInvestorsDailyTransactionTotal] ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')

    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[InstitutionalInvestorsDailyTransactionTotal] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        time.sleep(3)
        startDate = startDate + datetime.timedelta(1)

    db.close()