CREATE TABLE [dbo].[StockInfo] (
    [Id]         VARCHAR (20)   NOT NULL,
    [Name]       NVARCHAR (50)  NOT NULL,
    [ISIN_Code]  VARCHAR (50)   NULL,
    [StartDate]  DATE           NOT NULL,
    [MarketType] NVARCHAR (50)  NOT NULL,
    [Industry]   NVARCHAR (50)  NULL,
    [CFI_Code]   VARCHAR (50)   NULL,
    [Comment]    NVARCHAR (MAX) NULL, 
    [Type] NVARCHAR(50) NULL, 
    CONSTRAINT [PK_StockInfo] PRIMARY KEY ([Id])
);

