CREATE VIEW [dbo].[ForeignInvestersFutureContract]
	AS select TOP 60 A.Date, A.Who, A.LongShortTotalDiffCount + (B.LongShortTotalDiffCount / 4) Mix, A.LongShortTotalDiffCount AS AValue, B.LongShortTotalDiffCount AS BValue 
from FuturesContract A 
JOIN FuturesContract B ON A.Date = B.Date AND A.ProductName = N'臺股期貨' AND B.ProductName = N'小型臺指期貨' AND A.Who = B.Who
WHERE A.Who LIKE N'外資%'
