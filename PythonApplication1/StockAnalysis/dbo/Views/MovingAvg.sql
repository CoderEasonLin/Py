﻿CREATE VIEW [dbo].[MovingAvg]
	AS SELECT TOP 60 [Date],
       Taiex,
       ROUND(AVG(Taiex) OVER (ORDER BY Date ASC ROWS 59 PRECEDING), 2) AS MA60,
	   ROUND(AVG(Taiex) OVER (ORDER BY Date ASC ROWS 19 PRECEDING), 2) AS MA20,
	   ROUND(AVG(Taiex) OVER (ORDER BY Date ASC ROWS 4 PRECEDING), 2) AS MA5   
from TaiexDaily
order by Date DESC
