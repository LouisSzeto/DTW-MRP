#region imports
from AlgorithmImports import *
from BMRPortfolioConstructionModel import BMRPortfolioConstructionModel
from MeanReversionPortfolioConstructionModel import MeanReversionPortfolioConstructionModel
#endregion

class MeanReversionPortfolioAlgorithm(QCAlgorithm):

    # Selected assets
    ASSETS = {
        # Euclidean 2017
        1: ['AAPL', 'ACL', 'ADBE', 'ADSK', 'AEP', 'AET', 'AHA', 'ALB', 'ALGN', 'ALLE', 'AMAT', 'AMB', 'AME', 'AMGN', 'AMT', 'ANSS', 'AOC', 'AOS', 'ATVI', 'AVGO', 'BAX', 'BBY', 'BK', 'BSX', 'CBRNA', 'CDN', 'CERN', 'CEY', 'CINF', 'CMS', 'CNTE', 'COL', 'COO', 'CTSH', 'CUM', 'DLPH', 'DLR', 'DRE', 'DTE', 'DUK', 'EBAY', 'ECL', 'ED', 'EGG', 'EQIXD', 'EQR', 'ERTS', 'ETN', 'FB', 'FBHS', 'FISV', 'FMC', 'FPL', 'FTV', 'GART', 'GD', 'GLW', 'GOOCV', 'GOOG', 'GPN', 'HIG', 'HOU', 'HUM', 'HWP', 'IFF', 'ILMN', 'ISRG', 'JNJ', 'KO', 'KSU', 'LH', 'LMT', 'LRCX', 'MAA', 'MCD', 'MCHP', 'MGG', 'MHP', 'MMC', 'MON', 'MTD', 'NCLH', 'NFLX', 'NI', 'NSP', 'NU', 'NVDA', 'ORCL', 'PEP', 'PG', 'PKG', 'PNR', 'PNW', 'PVH', 'QRVO', 'RCL', 'ROP', 'RSG', 'RTNB', 'SBAC', 'SNPS', 'SRE', 'STT', 'SYK', 'TDG', 'TMO', 'TWRS', 'UDR', 'UTX', 'V', 'VAR', 'VRTX', 'WAT', 'WEC', 'WLTW', 'WPH', 'WYN', 'WYNN', 'XLNX', 'XRX', 'YUM'],
        # DTW 2017
        2: ['AAPL', 'ABT', 'ACL', 'ADBE', 'ADSK', 'AEE', 'AEP', 'AET', 'ALB', 'ALGN', 'ALLE', 'AMAT', 'AMB', 'AME', 'AMT', 'ANSS', 'AOC', 'AOS', 'ATVI', 'AVGO', 'BAX', 'BBY', 'BDX', 'CBRNA', 'CDN', 'CERN', 'CEY', 'CI', 'CLX', 'CMS', 'CNTE', 'COL', 'CRM', 'CSX', 'CTSH', 'CUM', 'DLPH', 'DNB', 'DTE', 'DUK', 'ECL', 'ED', 'EGG', 'EQIXD', 'ETN', 'ETR', 'FB', 'FBHS', 'FISV', 'FMC', 'FPL', 'FTV', 'GLW', 'GOOCV', 'GOOG', 'GPN', 'HIG', 'HOU', 'HWP', 'ICE', 'IFF', 'ILMN', 'ISRG', 'JNJ', 'KLAC', 'KO', 'KSU', 'LMT', 'LRCX', 'MA', 'MCD', 'MCHP', 'MHK', 'MHP', 'MMC', 'MTD', 'NFLX', 'NI', 'NSP', 'NU', 'NVDA', 'PKG', 'PNR', 'PNW', 'PPG', 'PVH', 'PYPL', 'RCL', 'RESM', 'RHAT', 'ROP', 'RTNB', 'SBAC', 'SNPS', 'SYK', 'TIF', 'TMO', 'TWRS', 'V', 'VAR', 'VRSN', 'VRTX', 'WAT', 'WEC', 'WLTW', 'WPH', 'WY', 'WYN', 'WYNN', 'XLNX'],
        # soft-DTW 2017
        3: ['AAPL', 'ADBE', 'ADSK', 'AEE', 'AEP', 'AET', 'AFL', 'ALB', 'ALGN', 'AMAT', 'AMB', 'AME', 'AMT', 'ANSS', 'AOC', 'AOS', 'ATVI', 'AVGO', 'BAX', 'BBY', 'CBRNA', 'CDN', 'CEY', 'CMS', 'CNTE', 'COL', 'CRM', 'CTSH', 'DLPH', 'DNB', 'DTE', 'DUK', 'ED', 'EGG', 'EQIXD', 'ETR', 'FB', 'FISV', 'FMC', 'FPL', 'FTV', 'GOOCV', 'GOOG', 'GPN', 'HIG', 'HOU', 'HUM', 'HWP', 'ICE', 'IFF', 'ILMN', 'ISRG', 'JNJ', 'KO', 'KSU', 'LMT', 'LRCX', 'MCD', 'MCHP', 'MHK', 'MHP', 'MMC', 'MTD', 'NFLX', 'NI', 'NRG', 'NSP', 'NU', 'NVDA', 'PKG', 'PNR', 'PNW', 'PVH', 'PYPL', 'RCL', 'ROP', 'RTNB', 'SBAC', 'SNPS', 'SRE', 'STT', 'SYK', 'TDG', 'TMO', 'TWRS', 'V', 'VAR', 'VRTX', 'WAT', 'WEC', 'WLTW', 'WPH', 'WYN', 'WYNN', 'XLNX', 'YUM'],
        # Euclidean 2019-20
        4: ['AAL', 'AFL', 'AIG', 'ALK', 'AVZ', 'BA', 'BK', 'CCL', 'CF', 'CFG', 'CHV', 'CMA', 'COF', 'COH', 'DAL', 'DFS', 'DISCA', 'DISCK', 'DVN', 'DXC', 'EOG', 'FANG', 'FES', 'FITB', 'FLIR', 'FLS', 'FRT', 'FTI', 'HBAN', 'HCN', 'HIG', 'HMT', 'HOC', 'HPE', 'HRB', 'KEY', 'KIM', 'KMI', 'KSS', 'LTR', 'LUV', 'LYV', 'MAR', 'MGG', 'MHK', 'MLM', 'MRO', 'MYL', 'NBL', 'NCLH', 'NLSN', 'NOB', 'NOI', 'NTAP', 'O', 'OKE', 'OMC', 'OXY', 'P', 'PBCT', 'PNC', 'PSX', 'PVH', 'RCL', 'REG', 'RGBK', 'SBC', 'SLB', 'SPG', 'SYY', 'TRV', 'TSN', 'UA', 'UARM', 'UAUA', 'UHS', 'UNM', 'USB', 'VFC', 'VLO', 'VNO', 'WAG', 'XON', 'XRX', 'ZION'],
        # DTW 2019-20
        5: ['AA', 'AAL', 'ACL', 'AFL', 'AHC', 'AIG', 'AIV', 'ALK', 'APA', 'AVZ', 'AXP', 'BA', 'BEN', 'BHGE', 'BYA', 'CCL', 'CF', 'CFG', 'CHV', 'CINF', 'CMA', 'COF', 'DAL', 'DFS', 'DRI', 'DVN', 'DXC', 'EOG', 'F', 'FANG', 'FITB', 'FLS', 'FLT', 'FRT', 'FTI', 'GD', 'GM', 'HAS', 'HBAN', 'HCN', 'HIG', 'HOU', 'HPE', 'HRB', 'KEY', 'KIM', 'KMI', 'KSS', 'LNC', 'LTR', 'LUV', 'LYB', 'LYV', 'MAR', 'MGG', 'MHK', 'MLM', 'MPC', 'MRO', 'NBL', 'NCLH', 'NLSN', 'NOI', 'O', 'OKE', 'OXY', 'P', 'PE', 'PRU', 'PSX', 'PVH', 'PXD', 'RCL', 'RE', 'REG', 'RGBK', 'SLB', 'SLG', 'SPC', 'SPG', 'SYF', 'SYY', 'TRV', 'TSN', 'UA', 'UARM', 'UAUA', 'UHS', 'UNM', 'USB', 'VC', 'VFC', 'VLO', 'XON', 'ZION'],
        # soft-DTW 2019-20
        6: ['AAL', 'AFL', 'AIG', 'AIV', 'ALK', 'AVZ', 'BA', 'BXP', 'BYA', 'CCL', 'CF', 'CFG', 'CHV', 'CMA', 'COF', 'COH', 'COTY', 'DAL', 'DVN', 'DXC', 'EOG', 'FANG', 'FES', 'FITB', 'FLIR', 'FLS', 'FRT', 'FTI', 'HBAN', 'HCN', 'HIG', 'HMT', 'HOC', 'HPE', 'HRB', 'KEY', 'KIM', 'KMI', 'KSS', 'LNC', 'LTR', 'LUV', 'LYV', 'MHK', 'MRO', 'NBL', 'NCLH', 'NLSN', 'NOB', 'NOI', 'OKE', 'OMC', 'OXY', 'P', 'PBCT', 'PNC', 'PSX', 'PVH', 'RCL', 'REG', 'RGBK', 'SBC', 'SLB', 'SLG', 'SPG', 'SYY', 'TRV', 'TSN', 'UA', 'UARM', 'UAUA', 'UHS', 'UNM', 'USB', 'VFC', 'VLO', 'VNO', 'WAG', 'XON', 'XRX', 'ZION']
    }
    PORTFOLIOS = {
        1: MeanReversionPortfolioConstructionModel(),
        2: BMRPortfolioConstructionModel()
    }   

    def Initialize(self):
        # Set starting date, cash and ending date of the backtest
        self.SetStartDate(2020, 9, 1)
        self.SetEndDate(2021, 8, 31)
        self.SetCash(100000)

        assets = self.ASSETS[int(self.GetParameter("assets"))]
        portfolio = self.PORTFOLIOS[int(self.GetParameter("portfolio"))]

        self.SetSecurityInitializer(lambda security: security.SetMarketPrice(self.GetLastKnownPrice(security)))
        
        # Subscribe to data of the selected stocks
        self.symbols = [self.AddEquity(ticker, Resolution.Daily).Symbol for ticker in assets]

        self.AddAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(1)))
        self.SetPortfolioConstruction(portfolio)
