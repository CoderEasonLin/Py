CREATE VIEW [dbo].[ForeignInvestorsTotal]
	AS SELECT TOP 60 [Date]
      ,[Who]
      ,[Buy] * 0.00000001 AS Buy
      ,[Sell] * 0.00000001 AS Sell
      ,[Diff] * 0.00000001 AS Diff
  FROM [dbo].[InstitutionalInvestorsDailyTransactionTotal]
  WHERE [Who] LIKE N'外資及陸資%'
  ORDER BY [Date] DESC