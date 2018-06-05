CREATE TABLE [dbo].[InstitutionalInvestorsDailyOptionSummary]
(
	[Date] DATE NOT NULL , 
    [ProductName] NVARCHAR(50) NOT NULL, 
    [Option] NVARCHAR(50) NOT NULL, 
    [Who] NVARCHAR(50) NOT NULL, 
    [Buy] INT NOT NULL, 
    [BuyTurnover] INT NOT NULL, 
    [Sell] INT NOT NULL, 
    [SellTurnover] INT NOT NULL, 
    [Diff] INT NOT NULL, 
    [DiffTurnover] INT NOT NULL, 
    [BuyTotal] INT NOT NULL, 
    [BuyTotalTurnover] INT NOT NULL, 
    [SellTotal] INT NOT NULL, 
    [SellTotalTurnover] INT NOT NULL, 
    [DiffTotal] INT NOT NULL, 
    [DiffTotalTurnover] INT NOT NULL, 
    PRIMARY KEY ([Date] DESC, [ProductName], [Option], [Who])
)
