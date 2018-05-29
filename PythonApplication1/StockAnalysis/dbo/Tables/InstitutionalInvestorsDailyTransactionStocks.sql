CREATE TABLE [dbo].[InstitutionalInvestorsDailyTransactionStocks]
(
	[Date] DATE NOT NULL , 
    [StockId] VARCHAR(20) NOT NULL, 
    [Who] NVARCHAR(50) NOT NULL, 
    [Buy] INT NOT NULL, 
    [Sell] INT NOT NULL, 
    [Diff] NCHAR(10) NOT NULL, 
    [HasBigTransaction] BIT NOT NULL, 
    PRIMARY KEY ([Date], [StockId], [Who])
)
