#!/usr/bin/env python
# encoding: utf-8
'''
@author: xiayidan
@desc: 使用pyalgotrade进行数据回测，详情：https://github.com/gbeced/pyalgotrade
'''

from pyalgotrade import strategy
from pyalgotrade_tushare import tools, barfeed
from pyalgotrade.technical import ma
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns


def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod1, smaPeriod2):
        super(MyStrategy, self).__init__(feed, 10000)  # 添加行情数据，以及买入金额
        self.__position = None
        self.__instrument = instrument
        # We want a 15 period SMA over the closing prices.
        self.__sma1 = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod1)
        self.__sma2 = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod2)

    def getSMA1(self):
        return self.__sma1

    def getSMA2(self):
        return self.__sma2

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        # self.info("BUY at ￥%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        # self.info("SELL at ￥%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma2[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if self.__sma1[-1] > self.__sma2[-1]:
                # Enter a buy market order for 100 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 100, True)
        # Check if we have to exit the position.
        elif self.__sma1[-1] < self.__sma2[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def run_strategy(smaPeriod1, smaPeriod2):
    # Load the bar feed from the CSV file
    instruments = ["000001"]
    feeds = tools.build_feed(instruments, 2018, 2021, "histdata")
    # print(feeds)

    # Evaluate the strategy with the feed's bars.
    myStrategy = MyStrategy(feeds, instruments[0], smaPeriod1, smaPeriod2)
    # myStrategy.run()
    # print(smaPeriod1, smaPeriod2, "Final portfolio value: ￥%.2f" % myStrategy.getBroker().getEquity())

    # 可视化部分
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)

    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("SMA1", myStrategy.getSMA1())
    plt.getInstrumentSubplot(instruments[0]).addDataSeries("SMA2", myStrategy.getSMA2())

    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    # Run the strategy.
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

    # Plot the strategy.
    plt.plot()


# 单均线
# for i in range(10, 30):
# 双均线
# ma1 = [5, 10, 15]
# ma2 = [15, 20, 30]
# for i in ma1:
#     for j in ma2:
#         if i < j:
#             run_strategy(i, j)

run_strategy(15, 30)
