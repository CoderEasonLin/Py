CREATE TABLE [dbo].[FuturesContract] (
    [Date]                       DATE      NOT NULL,
    [ProductName]                NVARCHAR (50) NOT NULL,
    [Who]                        NVARCHAR (50) NOT NULL,
    [LongCount]                  INT           NOT NULL,
    [LongTurnover]               INT           NOT NULL,
    [ShortCount]                 INT           NOT NULL,
    [ShortTurnover]              INT           NOT NULL,
    [LongShortDiffCount]         INT           NOT NULL,
    [LongShortDiffTurnover]      INT           NOT NULL,
    [LongTotalCount]             INT           NOT NULL,
    [LongTotalTurnover]          INT           NOT NULL,
    [ShortTotalCount]            INT           NOT NULL,
    [ShortTotalTurnover]         INT           NOT NULL,
    [LongShortTotalDiffCount]    INT           NOT NULL,
    [LongShortTotalDiffTurnover] INT           NOT NULL,
    CONSTRAINT [PK_FuturesContract] PRIMARY KEY CLUSTERED ([Date] DESC, [ProductName] ASC, [Who] ASC)
);

