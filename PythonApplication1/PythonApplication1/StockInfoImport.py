
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import os
import pymssql
import logging

def main():
    if not os.path.isdir('log'):
        os.makedirs('log')
    logging.basicConfig(filename='log/getlist-error.log',
                        level=logging.ERROR,
                        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    db = pymssql.connect(".", "sa", "sa", "StockAnalysis")
    cursor = db.cursor()

    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'lxml')

    try:
        deleteSql = "DELETE FROM StockInfo"
        cursor.execute(deleteSql)
        db.commit()

        kind = ""
        for row in soup.select('tr'):
            cols = row.find_all('td')
            data = re.search('(.*)　(.*)', cols[0].text)
            if data is not None:
                if data.group(1) is not None:
                    if data.group(2) is not None:
                        stockId = data.group(1).strip()
                        name = data.group(2).strip()
                        isinCode = cols[1].text.strip()
                        listingDate = cols[2].text.strip()
                        marketType = cols[3].text.strip()
                        industry = cols[4].text.strip()
                        cfiCode = cols[5].text.strip()
                        comment = cols[6].text.strip()
                        print(stockId, name, listingDate, industry)

                        try:
                            sql = "INSERT INTO [dbo].[StockInfo]\
                                   ([Id]\
                                   ,[Name]\
                                   ,[StartDate]\
                                   ,ISIN_Code\
                                   ,[CFI_Code]\
                                   ,Comment\
                                   ,[MarketType]\
                                   ,[Industry]\
                                   ,[Type])\
                                    VALUES ('%s', N'%s', '%s', '%s', '%s', N'%s', N'%s', N'%s', N'%s')" % \
                                  (stockId, name, listingDate, isinCode, cfiCode, comment, marketType, industry, kind)
                            cursor.execute(sql)
                            db.commit()
                        except Exception as e:
                            print(e)
                            logging.error("insert data error → StockId:" + stockId + ", RowData:" + str(data) + ", error msg:" + str(e))
                            db.rollback()
            else:
                print(cols.__len__())
                if cols.__len__() == 1 :
                    kind = cols[0].text.strip()


    except Exception as e:
        print(e)
        logging.error("delete or get data error → error msg:" + str(e))
    db.close()


if __name__ == '__main__':
    main()