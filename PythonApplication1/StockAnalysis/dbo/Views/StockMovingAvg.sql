﻿CREATE VIEW [dbo].[StockMovingAvg]
	AS SELECT [Date],
		StockId,
		ClosePrice,
		ROUND(AVG(ClosePrice) OVER (PARTITION BY StockId ORDER BY Date ASC ROWS 59 PRECEDING), 2) AS MA60,
		ROUND(AVG(ClosePrice) OVER (PARTITION BY StockId ORDER BY Date ASC ROWS 19 PRECEDING), 2) AS MA20,
		ROUND(AVG(ClosePrice) OVER (PARTITION BY StockId ORDER BY Date ASC ROWS 4 PRECEDING), 2) AS MA5   
from StockDaily
