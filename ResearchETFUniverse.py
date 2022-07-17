#region imports
from AlgorithmImports import *
#endregion
class ETFUniverse:
    """
    A class to create a universe of equities from the constituents of an ETF
    """
    def __init__(self, etf_ticker, universe_date):
        """
        Input:
         - etf_ticker
            Ticker of the ETF
         - universe_date
            The date to gather the constituents of the ETF
        """
        self.etf_ticker = etf_ticker
        self.universe_date = universe_date
    
    
    def get_symbols(self, qb):
        """
        Subscribes to the universe constituents and returns a list of symbols and their timezone
        
        Input:
         - qb
            The QuantBook instance inside the DatasetAnalyzer
        
        Returns a list of symbols and their timezone
        """
        etf_symbols = self._get_etf_constituents(qb, self.etf_ticker, self.universe_date)
        security_timezone = None
        security_symbols = []
        
        # Subscribe to the universe price data
        for symbol in etf_symbols:
            security = qb.AddSecurity(symbol, Resolution.Daily)
            security_timezone = security.Exchange.TimeZone
            security_symbols.append(symbol)
        
        return security_symbols, security_timezone
    
    
    def _get_etf_constituents(self, qb, etf_ticker, date):
        """
        A helper method to retreive the ETF constituents on a given date
        
        Input:
         - qb
            The QuantBook instance inside the DatasetAnalyzer
         - etf_ticker
             Ticker of the ETF
         - universe_date
            The date to gather the constituents of the ETF
        
        Returns a list of symbols
        """
        date_str = date.strftime("%Y%m%d")
        filename = f"/data/equity/usa/universes/etf/{etf_ticker.lower()}/{date_str}.csv"
        try:
            df = pd.read_csv(filename)
        except:
            print(f'Error: The ETF universe file does not exist')
            return
        security_ids = df[df.columns[1]].values
        symbols = [qb.Symbol(security_id) for security_id in security_ids]
        return symbols
