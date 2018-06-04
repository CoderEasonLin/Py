CREATE PROCEDURE [dbo].[ContinueBuy]
	@days int,
	@date DATE,
	@who  NVARCHAR(50)
AS
	DECLARE @rows INT = @days - 1;

	EXEC ('select * from (
	SELECT [Date]
      ,[StockId]
      ,[Who]
      ,[Diff]
	  ,SUM(CASE WHEN Diff > 0 THEN 1 ELSE 0 END) OVER (PARTITION BY StockId, Who ORDER BY Date ASC ROWS ' + @rows + ' PRECEDING) AS Days
	FROM [StockAnalysis].[dbo].[InstitutionalInvestorsDailyTransactionStocks]
	where  Who LIKE N''' + @who + '%'') a
	where Days = ' + @days + ' and Date = ''' + @date + '''')
RETURN 0
