#region imports
from AlgorithmImports import *
from MeanReversionPortfolioConstructionModel import MeanReversionPortfolioConstructionModel
from tslearn.barycenters import dtw_barycenter_averaging
#endregion

class BMRPortfolioConstructionModel(MeanReversionPortfolioConstructionModel):
    '''Implementation of Mean Reversion towards Barycenter'''

    def __init__(self,
                 eps = 1,
                 window_size = 20,
                 resolution = Resolution.Daily):
        """Initialize the model
        Args:
            eps: Reversion threshold
            window_size: window size of MA
            resolution: The resolution of the history price and rebalancing
        """
        super().__init__(eps, resolution)
        self.window_size = window_size
        np.random.seed(0)

    def OnSecuritiesChanged(self, algorithm, changes):
        """Event fired each time the we add/remove securities from the data feed
        Args:
            algorithm: The algorithm instance that experienced the change in securities
            changes: The security additions and removals from the algorithm
        """
        # clean up data for removed securities
        for removed in changes.RemovedSecurities:
            symbol_data = self.symbol_data.pop(removed.Symbol, None)
            symbol_data.Reset()

        # initialize data for added securities
        symbols = [ x.Symbol for x in changes.AddedSecurities ]

        for symbol in symbols:
            if symbol not in self.symbol_data:
                self.symbol_data[symbol] = SymbolData(algorithm, symbol, self.window_size, self.resolution)

    def Prediction(self, insights):
        # Get barycenter
        df = pd.DataFrame({insight.Symbol: self.symbol_data[insight.Symbol].window for insight in insights})
        log_df = np.log(df)
        standard_df = (log_df - log_df.mean(axis=0))/log_df.std(axis=0)
        transform_df = standard_df.T.values

        barycenter = dtw_barycenter_averaging(transform_df, max_iter=5)
        
        # Use the last standard log price / datapoint of the barycenter as price relative
        # Un-standardize barycenter value for scaling
        relatives = standard_df.values[-1] / (barycenter[-1] * log_df.std(axis=0) + log_df.mean(axis=0)).replace([np.inf, -np.inf, np.nan], 0)

        return np.asarray(relatives).flatten()
            
class SymbolData:
    def __init__(self, algo, symbol, window_size, resolution):
        # Indicator of price
        self.identity = algo.Identity(symbol, resolution)
        # Initialize a moving average indicator
        self.window = RollingWindow[float](window_size)

        # Warmup indicator
        history = algo.History(symbol, window_size, resolution)
        for row in history.itertuples():
            self.window.Add(row.close)

        # Set auto-update on RollingWindow
        self.identity.Updated += lambda sender, update: self.window.Add(update.Value)

    def Reset(self):
        self.identity.Reset()
        self.window.Reset()
    
    @property
    def IsReady(self):
        return (self.identity.IsReady & self.window.IsReady)
