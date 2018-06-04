CREATE TABLE [dbo].[BigInvestorsFutureContract]
(
	[Date] DATE NOT NULL , 
    [ProductName] NVARCHAR(50) NOT NULL, 
    [Deadline] NVARCHAR(50) NOT NULL, 
    [BuyTop5] INT NOT NULL, 
    [BuyTop10] INT NOT NULL, 
    [SellTop5] INT NOT NULL, 
    [SellTop10] INT NOT NULL, 
    [Total] INT NOT NULL, 
    PRIMARY KEY ([Date] DESC, [ProductName], [Deadline])
)
