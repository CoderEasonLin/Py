CREATE TABLE [dbo].[InstitutionalInvestorsDailyTransactionStocks]
(
	[Date] DATE NOT NULL , 
    [StockId] VARCHAR(20) NOT NULL, 
    [Who] NVARCHAR(50) NOT NULL, 
    [Buy] INT NOT NULL, 
    [Sell] INT NOT NULL, 
    [Diff] INT NOT NULL, 
    PRIMARY KEY ([Date], [StockId], [Who])
)
