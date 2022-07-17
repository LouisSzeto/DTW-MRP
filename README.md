# DTW-MRP
Source code of WQU MScFE Capstone Project:

- A Mean-Reverting Portfolio with DTW Clustering

These source codes were meant to be incorporate into QuantConnect's LEAN algorithmic trading engine (master v14273). Results in the research were drawn from Optimization function in QC's cloud IDE. Any usage is allowed with credit awarded to the author. However, the author would not be responsible on any loss resulted from using the codes/method described in the research.

### Abstract
Current mean reversion assumed instantaneous reversion towards an expected price level, and the competition in this field was getting fiercer in the high-frequency/low-latency field, ranging from more alternative information sources to faster prediction and execution systems. However, markets were mostly in semi-efficient form only, delayed price changes were easily observable with lots of different information flooding the market. DTW clustering stock selection and barycenter mean reverting portfolio strategies were proposed to capture this horizontal spread, on top of the vertical spread of between-asset price mismatch. Results showed both factors could boost portfolio return, Sharpe Ratio, and Information Ratio regardless of the market regime. This implied the plausibility of slow arbitrage from delayed price action.
