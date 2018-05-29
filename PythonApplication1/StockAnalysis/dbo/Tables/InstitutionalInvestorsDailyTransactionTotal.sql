CREATE TABLE [dbo].[InstitutionalInvestorsDailyTransaction]
(
	[Date] DATE NOT NULL , 
    [Who] NVARCHAR(50) NOT NULL, 
    [Buy] BIGINT NOT NULL, 
    [Sell] BIGINT NOT NULL, 
    [Diff] BIGINT NOT NULL, 
    PRIMARY KEY ([Date], [Who])
)
