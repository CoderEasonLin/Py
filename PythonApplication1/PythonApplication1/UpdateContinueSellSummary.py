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
    try:
        cursor.execute("EXECUTE [dbo].[InsertContinueSellSummary] N'外資' ,'%s'" % dateStrToDB)
        db.commit()

        cursor.execute("EXECUTE [dbo].[InsertContinueSellSummary] N'投信' ,'%s'" % dateStrToDB)
        db.commit()
        
        cursor.execute("EXECUTE [dbo].[InsertContinueSellSummary] N'自營商' ,'%s'" % dateStrToDB)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

if __name__ == '__main__':
    # 爬電腦當天的資料
    startDate = None
    nowDate = datetime.datetime.now()

    if startDate is None:
        cursor.execute("SELECT TOP 1 Date FROM [ContinueSellSummary] ORDER BY Date DESC")
        row = cursor.fetchone()
        startDate = nowDate if row is None else datetime.datetime.strptime(row[0], '%Y-%m-%d')

    while startDate <= nowDate:
        print(startDate)

        # remove data before insert
        cursor.execute("DELETE FROM [dbo].[ContinueSellSummary] WHERE Date = '%s'" % (startDate.strftime("%Y/%m/%d")))
        db.commit()

        main(startDate)
        startDate = startDate + datetime.timedelta(1)

    db.close()