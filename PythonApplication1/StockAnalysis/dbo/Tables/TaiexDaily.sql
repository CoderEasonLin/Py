CREATE TABLE [dbo].[TaiexDaily]
(
	[Date] DATE NOT NULL PRIMARY KEY, 
    [TradingShares] BIGINT NOT NULL, 
    [TradingTurnover] BIGINT NOT NULL, 
    [Transaction] INT NOT NULL, 
    [Taiex] DECIMAL(9, 2) NOT NULL, 
    [Diff] DECIMAL(9, 2) NOT NULL
)
