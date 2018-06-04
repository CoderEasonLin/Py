CREATE PROCEDURE [dbo].[InsertContinueBuySummary]
	@who  NVARCHAR(50),
	@date DATE = NULL
AS
	IF @date IS NULL
	BEGIN
		SELECT @date = MAX(Date) FROM dbo.InstitutionalInvestorsDailyTransactionStocks
	END

	CREATE TABLE #summary (Date DATE, StockId VARCHAR(20), Who NVARCHAR(50), Diff INT, Days INT)

	DECLARE @Days INT = 1
	
	WHILE(@Days <= 50)
	BEGIN 
		INSERT #summary
		EXEC dbo.ContinueBuy @Days, @date, @who

		IF @@ROWCOUNT = 0
			BREAK;

		SET @Days = @Days + 1
	END

	INSERT dbo.ContinueBuySummary
	SELECT Date, StockId, Who, Diff, MAX(Days) AS Days FROM #summary
	GROUP BY Date, StockId, Who, Diff
RETURN 0
