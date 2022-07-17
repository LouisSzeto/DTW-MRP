#region imports
from AlgorithmImports import *
#endregion

class MeanReversionPortfolioConstructionModel(PortfolioConstructionModel):
    """Implementation of Passive Aggressive Mean Reversion portfolio from
    B. Li, P. Zhao, S.C.H. Hoi, V. Gopalkrishnan. (2012) Pamr: passive aggressive mean reversion strategy for portfolio selection. Mach. Learn., 87 (2), pp. 221-258
    Available at https://link.springer.com/content/pdf/10.1007/s10994-012-5281-z.pdf
    """
    def __init__(self,
                 eps = 1,
                 resolution = Resolution.Daily):
        """Initialize the model
        Args:
            eps: Reversion threshold
            resolution: The resolution of the history price and rebalancing
        """
        super().__init__()
        self.eps = eps
        self.resolution = resolution
        self.m = 0

        # Initialize a dictionary to store stock data
        self.symbol_data = {}

    def DetermineTargetPercent(self, activeInsights):
        """Will determine the target percent for each insight
        Args:
            activeInsights: list of active insights
        Returns:
            dictionary of insight and respective target weight
        """
        targets = {}

        # If we have no insights or non-ready just return an empty target list
        if len(activeInsights) == 0 or not all([self.symbol_data[x.Symbol].IsReady for x in activeInsights]):
            return targets

        m = len(activeInsights)
        if m != self.m:
            self.m = m
            # Initialize portfolio weightings vector
            self.b_t = np.ones(m) * (1/m)

        ### Get next price relative predictions in PAMR
        x_tilde = self.Prediction(activeInsights)

        ### Get step size of next portfolio
        # \bar{x}_{t+1} = 1^T * \tilde{x}_{t+1} / m
        # \lambda_{t+1} = max( 0, ( b_t * \tilde{x}_{t+1} - \epsilon ) / ||\tilde{x}_{t+1}  - \bar{x}_{t+1} * 1|| ^ 2 )
        x_bar = x_tilde.mean()
        assets_mean_dev = x_tilde - x_bar
        second_norm = (np.linalg.norm(assets_mean_dev)) ** 2
        
        if second_norm == 0.0:
            step_size = 0
        else:
            step_size = (np.dot(self.b_t, x_tilde) - self.eps) / second_norm
            step_size = max(0, step_size)

        ### Get next portfolio weightings
        # b_{t+1} = b_t - step_size * ( \tilde{x}_{t+1}  - \bar{x}_{t+1} * 1 )
        b = self.b_t - step_size * assets_mean_dev
        # Normalize
        b_norm = self.SimplexProjection(b)
        self.b_t = b_norm

        for i, insight in enumerate(activeInsights):
            targets[insight] = b_norm[i]

        return targets

    def OnSecuritiesChanged(self, algorithm, changes):
        """Event fired each time the we add/remove securities from the data feed
        Args:
            algorithm: The algorithm instance that experienced the change in securities
            changes: The security additions and removals from the algorithm
        """
        # clean up data for removed securities
        super().OnSecuritiesChanged(algorithm, changes)
        for removed in changes.RemovedSecurities:
            symbol_data = self.symbol_data.pop(removed.Symbol, None)
            symbol_data.Reset()

        # initialize data for added securities
        symbols = [ x.Symbol for x in changes.AddedSecurities ]

        for symbol in symbols:
            if symbol not in self.symbol_data:
                self.symbol_data[symbol] = SymbolData(algorithm, symbol, self.resolution)

    def Prediction(self, insights):
        # Initialize a price vector of the next prices relatives' projection
        x_tilde = np.zeros(len(insights))

        # Using the previous price to simulate assumption of instant reversion
        for i, insight in enumerate(insights):
            if insight.Magnitude is not None:
                x_tilde[i] = 1 + insight.Magnitude
            else:
                window = self.symbol_data[insight.Symbol].window
                x_tilde[i] = window[0] / window[1]

        return x_tilde

    def SimplexProjection(self, v, b=1):
        """Normalize the updated portfolio into weight vector:
        v_{t+1} = arg min || v - v_{t+1} || ^ 2
        
        Implementation from:
        Duchi, J., Shalev-Shwartz, S., Singer, Y., & Chandra, T. (2008, July). 
            Efficient projections onto the l 1-ball for learning in high dimensions.
            In Proceedings of the 25th international conference on Machine learning 
            (pp. 272-279).
        """
        v = np.asarray(v)

        # Sort v into u in descending order
        u = np.sort(v)[::-1]
        sv = np.cumsum(u)

        rho = np.where(u > (sv - b) / np.arange(1, len(v) + 1))[0][-1]
        theta = (sv[rho] - b) / (rho + 1)
        w = (v - theta)
        w[w < 0] = 0
        return w

class SymbolData:
    def __init__(self, algo, symbol, resolution):
        # Indicator of price
        self.identity = algo.Identity(symbol, resolution)
        # RollingWindow storing 2 last prices
        self.window = RollingWindow[float](2)

        # Update RollingWindow by Identity indicator
        self.identity.Updated += self.OnIdentity
        # Warmup indicator
        algo.WarmUpIndicator(symbol, self.identity, resolution)

    def OnIdentity(self, sender, updated):
        self.window.Add(updated.Value)

    def Reset(self):
        self.identity.Updated -= self.OnIdentity
        self.identity.Reset()
        self.window.Reset()
    
    @property
    def IsReady(self):
        return self.window.IsReady
