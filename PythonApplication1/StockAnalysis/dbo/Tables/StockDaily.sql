CREATE TABLE [dbo].[StockDaily]
(
	[Date] DATE NOT NULL , 
    [StockId] VARCHAR(20) NOT NULL, 
    [TradingShare] BIGINT NOT NULL, 
    [Transaction] INT NOT NULL, 
    [Turnover] BIGINT NOT NULL, 
    [OpenPrice] DECIMAL(7, 2) NOT NULL, 
    [DayHigh] DECIMAL(7, 2) NOT NULL, 
    [DayLow] DECIMAL(7, 2) NOT NULL, 
    [ClosePrice] DECIMAL(7, 2) NOT NULL, 
    [UpDown] DECIMAL(7, 2) NOT NULL, 
    [LastBuyPrice] DECIMAL(7, 2) NOT NULL, 
    [LastBuyCount] INT NOT NULL, 
    [LastSellPrice] DECIMAL(7, 2) NOT NULL, 
    [LastSellCount] INT NOT NULL, 
    [PER] DECIMAL(7, 2) NOT NULL, 
    PRIMARY KEY ([Date] DESC, [StockId])
)
