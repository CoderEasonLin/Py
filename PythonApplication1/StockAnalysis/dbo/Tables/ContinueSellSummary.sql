CREATE TABLE [dbo].[ContinueSellSummary]
(
	[Date] DATE NOT NULL , 
    [StockId] VARCHAR(20) NOT NULL, 
    [Who] NVARCHAR(50) NOT NULL, 
    [Diff] INT NOT NULL, 
    [Days] INT NOT NULL, 
    PRIMARY KEY ([Date], [StockId], [Who])
)
