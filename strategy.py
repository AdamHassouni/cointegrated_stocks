from AlgorithmImports import *
import numpy as np
from collections import deque
from math import floor

class CointegrationBollingerBandsStrategy(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2022, 1, 1)
        self.SetEndDate(2024, 9, 1)
        self.SetCash(500000)
        
        self.lookback = 15
        self.entry_z = 1.5
        self.exit_z = 0.5
        self.base_quantity = 1  # Further reduced base quantity
        
        self.weights = np.array([1.0, -1.213])
        
        self.tickers = ["NVDA", "BOTZ"]
        self.symbols = [self.AddEquity(ticker, Resolution.Daily).Symbol for ticker in self.tickers]
        
        self.latest_prices = np.full(len(self.tickers), -1.0)
        self.port_mkt_val = deque(maxlen=self.lookback)
        self.invested = None
        self.bars_elapsed = 0
        self.threshold = 1.0
        
        for symbol in self.symbols:
            symbol.hist_window = RollingWindow[TradeBar](self.lookback)
    
    def OnData(self, data):
        if not all(data.ContainsKey(symbol) for symbol in self.symbols):
            return

        for symbol in self.symbols:
            symbol.hist_window.Add(data[symbol])
        
        if self.symbols[0].hist_window.Count < self.lookback:
            return
        
        self._update_latest_prices(data)
        
        if all(self.latest_prices > -1.0):
            self.port_mkt_val.append(np.dot(self.latest_prices, self.weights))
            
            if self.bars_elapsed > self.lookback:
                zscore = (self.port_mkt_val[-1] - np.mean(self.port_mkt_val)) / np.std(self.port_mkt_val)
                self.Debug(f"Calculated Z-score: {zscore} on {data[self.symbols[0]].EndTime}")
                self.zscore_trade(zscore, data[self.symbols[0]].EndTime)
        
        self.bars_elapsed += 1
    
    def _update_latest_prices(self, data):
        for i, symbol in enumerate(self.symbols):
            self.latest_prices[i] = data[symbol].Close
        self.Debug(f"Updated latest prices: {self.latest_prices}")
            
    def go_long_units(self):
        for i, symbol in enumerate(self.symbols):
            quantity = int(floor(self.base_quantity * abs(self.weights[i])))
            if self.weights[i] < 0.0:
                self.SetHoldings(symbol, -self.base_quantity * self.weights[i])
                self.Debug(f"Selling {quantity} units of {symbol}")
            else:
                self.SetHoldings(symbol, self.base_quantity * self.weights[i])
                self.Debug(f"Buying {quantity} units of {symbol}")
                
    def go_short_units(self):
        for i, symbol in enumerate(self.symbols):
            quantity = int(floor(self.base_quantity * abs(self.weights[i])))
            if self.weights[i] < 0.0:
                self.SetHoldings(symbol, self.base_quantity * self.weights[i])
                self.Debug(f"Buying {quantity} units of {symbol}")
            else:
                self.SetHoldings(symbol, -self.base_quantity * self.weights[i])
                self.Debug(f"Selling {quantity} units of {symbol}")
                
    def zscore_trade(self, zscore, current_time):
        self.Debug(f"Z-score: {zscore} at {current_time}, invested state: {self.invested}")
        if self.invested is None:
            if zscore < -self.entry_z:
                self.go_long_units()
                self.invested = "long"
                self.Debug(f"Entering long position at {current_time}")
            elif zscore > self.entry_z:
                self.go_short_units()
                self.invested = "short"
                self.Debug(f"Entering short position at {current_time}")
        elif self.invested == "long" and zscore >= -self.exit_z:
            self.go_short_units()
            self.invested = None
            self.Debug(f"Exiting long position at {current_time}")
        elif self.invested == "short" and zscore <= self.exit_z:
            self.go_long_units()
            self.invested = None
            self.Debug(f"Exiting short position at {current_time}")

    def OnEndOfAlgorithm(self):
        self.Debug(f"Final Portfolio Value: {self.Portfolio.TotalPortfolioValue}")


#you have to run this code on  https://www.quantconnect.com 