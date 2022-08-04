# awesome-quant

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of insanely awesome libraries, packages and resources for Quants (Quantitative Finance)

## Languages

- [Python](#python)
- [R](#r)
- [Matlab](#matlab)
- [Julia](#julia)
- [Java](#java)
- [JavaScript](#javascript)
- [Haskell](#haskell)
- [Scala](#scala)
- [Ruby](#ruby)
- [Elixir/Erlang](#elixirerlang)
- [Golang](#golang)
- [CPP](#cpp)
- [CSharp](#csharp)
- [Rust](#rust)
- [Frameworks](#frameworks)
- [Reproducing Works](#reproducing-works)

## Python

### Numerical Libraries & Data Structures

- [numpy](https://www.numpy.org) - NumPy is the fundamental package for scientific computing with Python.
- [scipy](https://www.scipy.org) - SciPy (pronounced “Sigh Pie”) is a Python-based ecosystem of open-source software for mathematics, science, and engineering.
- [pandas](https://pandas.pydata.org) - pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
- [quantdsl](https://github.com/johnbywater/quantdsl) - Domain specific language for quantitative analytics in finance and trading.
- [statistics](https://docs.python.org/3/library/statistics.html) - Builtin Python library for all basic statistical calculations.
- [sympy](https://www.sympy.org/) - SymPy is a Python library for symbolic mathematics.
- [pymc3](https://docs.pymc.io/) - Probabilistic Programming in Python: Bayesian Modeling and Probabilistic Machine Learning with Theano.

### Financial Instruments and Pricing

- [OpenBB Terminal](https://github.com/OpenBB-finance/OpenBBTerminal) - Terminal for investment research for everyone.
- [PyQL](https://github.com/enthought/pyql) - QuantLib's Python port.
- [pyfin](https://github.com/opendoor-labs/pyfin) - Basic options pricing in Python. [ARCHIVED]
- [vollib](https://github.com/vollib/vollib) - vollib is a python library for calculating option prices, implied volatility and greeks.
- [QuantPy](https://github.com/jsmidt/QuantPy) - A framework for quantitative finance In python.
- [Finance-Python](https://github.com/alpha-miner/Finance-Python) - Python tools for Finance.
- [ffn](https://github.com/pmorissette/ffn) - A financial function library for Python.
- [pynance](https://github.com/GriffinAustin/pynance) - Lightweight Python library for assembling and analysing financial data.
- [tia](https://github.com/bpsmith/tia) - Toolkit for integration and analysis.
- [hasura/base-python-dash](https://platform.hasura.io/hub/projects/hasura/base-python-dash) - Hasura quickstart to deploy Dash framework. Written on top of Flask, Plotly.js, and React.js, Dash is ideal for building data visualization apps with highly custom user interfaces in pure Python.
- [hasura/base-python-bokeh](https://platform.hasura.io/hub/projects/hasura/base-python-bokeh) - Hasura quickstart to visualize data with bokeh library.
- [pysabr](https://github.com/ynouri/pysabr) - SABR model Python implementation.
- [FinancePy](https://github.com/domokane/FinancePy) - A Python Finance Library that focuses on the pricing and risk-management of Financial Derivatives, including fixed-income, equity, FX and credit derivatives.
- [gs-quant](https://github.com/goldmansachs/gs-quant) - Python toolkit for quantitative finance
- [willowtree](https://github.com/federicomariamassari/willowtree) - Robust and flexible Python implementation of the willow tree lattice for derivatives pricing.
- [financial-engineering](https://github.com/federicomariamassari/financial-engineering) - Applications of Monte Carlo methods to financial engineering projects, in Python.
- [optlib](https://github.com/dbrojas/optlib) - A library for financial options pricing written in Python.
- [tf-quant-finance](https://github.com/google/tf-quant-finance) - High-performance TensorFlow library for quantitative finance.
- [Q-Fin](https://github.com/RomanMichaelPaolucci/Q-Fin) - A Python library for mathematical finance.
- [Quantsbin](https://github.com/quantsbin/Quantsbin) - Tools for pricing and plotting of vanilla option prices, greeks and various other analysis around them.
- [finoptions](https://github.com/bbcho/finoptions-dev) - Complete python implementation of R package fOptions with partial implementation of fExoticOptions for pricing various options.

### Indicators

- [pandas_talib](https://github.com/femtotrader/pandas_talib) - A Python Pandas implementation of technical analysis indicators.
- [finta](https://github.com/peerchemist/finta) - Common financial technical analysis indicators implemented in Pandas.
- [Tulipy](https://github.com/cirla/tulipy) - Financial Technical Analysis Indicator Library (Python bindings for [tulipindicators](https://github.com/TulipCharts/tulipindicators))
- [lppls](https://github.com/Boulder-Investment-Technologies/lppls) - A Python module for fitting the [Log-Periodic Power Law Singularity (LPPLS)](https://en.wikipedia.org/wiki/Didier_Sornette#The_JLS_and_LPPLS_models) model.

### Trading & Backtesting

- [Blankly](https://github.com/Blankly-Finance/Blankly) - Fully integrated backtesting, paper trading, and live deployment.
- [TA-Lib](https://github.com/mrjbq7/ta-lib) - Python wrapper for TA-Lib (http://ta-lib.org/).
- [zipline](https://github.com/quantopian/zipline) - Pythonic algorithmic trading library.
- [QuantSoftware Toolkit](https://github.com/QuantSoftware/QuantSoftwareToolkit) - Python-based open source software framework designed to support portfolio construction and management.
- [quantitative](https://github.com/jeffrey-liang/quantitative) - Quantitative finance, and backtesting library.
- [analyzer](https://github.com/llazzaro/analyzer) - Python framework for real-time financial and backtesting trading strategies.
- [bt](https://github.com/pmorissette/bt) - Flexible Backtesting for Python.
- [backtrader](https://github.com/backtrader/backtrader) - Python Backtesting library for trading strategies.
- [pythalesians](https://github.com/thalesians/pythalesians) - Python library to backtest trading strategies, plot charts, seamlessly download market data, analyse market patterns etc.
- [pybacktest](https://github.com/ematvey/pybacktest) - Vectorized backtesting framework in Python / pandas, designed to make your backtesting easier.
- [pyalgotrade](https://github.com/gbeced/pyalgotrade) - Python Algorithmic Trading Library.
- [tradingWithPython](https://pypi.org/project/tradingWithPython/) - A collection of functions and classes for Quantitative trading.
- [Pandas TA](https://github.com/twopirllc/pandas-ta) - Pandas TA is an easy to use Python 3 Pandas Extension with 115+ Indicators. Easily build Custom Strategies.
- [ta](https://github.com/bukosabino/ta) - Technical Analysis Library using Pandas (Python)
- [algobroker](https://github.com/joequant/algobroker) - This is an execution engine for algo trading.
- [pysentosa](https://pypi.org/project/pysentosa/) - Python API for sentosa trading system.
- [finmarketpy](https://github.com/cuemacro/finmarketpy) - Python library for backtesting trading strategies and analyzing financial markets.
- [binary-martingale](https://github.com/metaperl/binary-martingale) - Computer program to automatically trade binary options martingale style.
- [fooltrader](https://github.com/foolcage/fooltrader) - the project using big-data technology to provide an uniform way to analyze the whole market.
- [zvt](https://github.com/zvtvz/zvt) - the project using sql,pandas to provide an uniform and extendable way to record data,computing factors,select securites, backtesting,realtime trading and it could show all of them in clearly charts in realtime.
- [pylivetrader](https://github.com/alpacahq/pylivetrader) - zipline-compatible live trading library.
- [pipeline-live](https://github.com/alpacahq/pipeline-live) - zipline's pipeline capability with IEX for live trading.
- [zipline-extensions](https://github.com/quantrocket-llc/zipline-extensions) - Zipline extensions and adapters for QuantRocket.
- [moonshot](https://github.com/quantrocket-llc/moonshot) - Vectorized backtester and trading engine for QuantRocket based on Pandas.
- [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) - Financial portfolio optimisation in python, including classical efficient frontier and advanced methods.
- [Eiten](https://github.com/tradytics/eiten) - Eiten is an open source toolkit by Tradytics that implements various statistical and algorithmic investing strategies such as Eigen Portfolios, Minimum Variance Portfolios, Maximum Sharpe Ratio Portfolios, and Genetic Algorithms based Portfolios.
- [riskparity.py](https://github.com/dppalomar/riskparity.py) - fast and scalable design of risk parity portfolios with TensorFlow 2.0
- [mlfinlab](https://github.com/hudson-and-thames/mlfinlab) - Implementations regarding "Advances in Financial Machine Learning" by Marcos Lopez de Prado. (Feature Engineering, Financial Data Structures, Meta-Labeling)
- [pyqstrat](https://github.com/abbass2/pyqstrat) - A fast, extensible, transparent python library for backtesting quantitative strategies.
- [NowTrade](https://github.com/edouardpoitras/NowTrade) - Python library for backtesting technical/mechanical strategies in the stock and currency markets.
- [pinkfish](https://github.com/fja05680/pinkfish) - A backtester and spreadsheet library for security analysis.
- [aat](https://github.com/timkpaine/aat) - Async Algorithmic Trading Engine
- [Backtesting.py](https://kernc.github.io/backtesting.py/) - Backtest trading strategies in Python
- [catalyst](https://github.com/enigmampc/catalyst) - An Algorithmic Trading Library for Crypto-Assets in Python
- [quantstats](https://github.com/ranaroussi/quantstats) - Portfolio analytics for quants, written in Python
- [qtpylib](https://github.com/ranaroussi/qtpylib) - QTPyLib, Pythonic Algorithmic Trading <http://qtpylib.io>
- [Quantdom](https://github.com/constverum/Quantdom) - Python-based framework for backtesting trading strategies & analyzing financial markets [GUI :neckbeard:]
- [freqtrade](https://github.com/freqtrade/freqtrade) - Free, open source crypto trading bot
- [algorithmic-trading-with-python](https://github.com/chrisconlan/algorithmic-trading-with-python) - Free `pandas` and `scikit-learn` resources for trading simulation, backtesting, and machine learning on financial data.
- [DeepDow](https://github.com/jankrepl/deepdow) - Portfolio optimization with deep learning
- [Qlib](https://github.com/microsoft/qlib) - An AI-oriented Quantitative Investment Platform by Microsoft. Full ML pipeline of data processing, model training, back-testing; and covers the entire chain of quantitative investment: alpha seeking, risk modeling, portfolio optimization, and order execution.
- [machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) - Code and resources for Machine Learning for Algorithmic Trading
- [AlphaPy](https://github.com/ScottfreeLLC/AlphaPy) - Automated Machine Learning [AutoML] with Python, scikit-learn, Keras, XGBoost, LightGBM, and CatBoost
- [jesse](https://github.com/jesse-ai/jesse) - An advanced crypto trading bot written in Python
- [rqalpha](https://github.com/ricequant/rqalpha) - A extendable, replaceable Python algorithmic backtest && trading framework supporting multiple securities.
- [FinRL-Library](https://github.com/AI4Finance-LLC/FinRL-Library) - A Deep Reinforcement Learning Library for Automated Trading in Quantitative Finance. NeurIPS 2020.
- [bulbea](https://github.com/achillesrasquinha/bulbea) - Deep Learning based Python Library for Stock Market Prediction and Modelling.
- [ib_nope](https://github.com/ajhpark/ib_nope) - Automated trading system for NOPE strategy over IBKR TWS.
- [OctoBot](https://github.com/Drakkar-Software/OctoBot) - Open source cryptocurrency trading bot for high frequency, arbitrage, TA and social trading with an advanced web interface.
- [bta-lib](https://github.com/mementum/bta-lib) - Technical Analysis library in pandas for backtesting algotrading and quantitative analysis.
- [Stock-Prediction-Models](https://github.com/huseinzol05/Stock-Prediction-Models) - Gathers machine learning and deep learning models for Stock forecasting including trading bots and simulations.
- [TuneTA](https://github.com/jmrichardson/tuneta) - TuneTA optimizes technical indicators using a distance correlation measure to a user defined target feature such as next day return.
- [AutoTrader](https://github.com/kieran-mackle/AutoTrader) - A Python-based development platform for automated trading systems - from backtesting to optimisation to livetrading.
- [fast-trade](https://github.com/jrmeier/fast-trade) - A library built with backtest portability and performance in mind for backtest trading strategies.
- [qf-lib](https://github.com/quarkfin/qf-lib) - QF-Lib is a Python library that provides high quality tools for quantitative finance.
- [tda-api](https://github.com/alexgolec/tda-api) - Gather data and trade equities, options, and ETFs via TDAmeritrade.
- [vectorbt](https://github.com/polakowo/vectorbt) - Find your trading edge, using a powerful toolkit for backtesting, algorithmic trading, and research.
- [Lean](https://github.com/QuantConnect/Lean) - Lean Algorithmic Trading Engine by QuantConnect (Python, C#).
- [fast-trade](https://github.com/jrmeier/fast-trade) - Low code backtesting library utilizing pandas and technical analysis indicators.

### Risk Analysis

- [pyfolio](https://github.com/quantopian/pyfolio) - Portfolio and risk analytics in Python.
- [empyrical](https://github.com/quantopian/empyrical) - Common financial risk and performance metrics.
- [fecon235](https://github.com/rsvp/fecon235) - Computational tools for financial economics include: Gaussian Mixture model of leptokurtotic risk, adaptive Boltzmann portfolios.
- [finance](https://pypi.org/project/finance/) - Financial Risk Calculations. Optimized for ease of use through class construction and operator overload.
- [qfrm](https://pypi.org/project/qfrm/) - Quantitative Financial Risk Management: awesome OOP tools for measuring, managing and visualizing risk of financial instruments and portfolios.
- [visualize-wealth](https://github.com/benjaminmgross/visualize-wealth) - Portfolio construction and quantitative analysis.
- [VisualPortfolio](https://github.com/wegamekinglc/VisualPortfolio) - This tool is used to visualize the perfomance of a portfolio.
- [universal-portfolios](https://github.com/Marigold/universal-portfolios) - Collection of algorithms for online portfolio selection.
- [FinQuant](https://github.com/fmilthaler/FinQuant) - A program for financial portfolio management, analysis and optimisation.
- [Empyrial](https://github.com/ssantoshp/Empyrial) - Portfolio's risk and performance analytics and returns predictions.
- [risktools](https://github.com/bbcho/risktools-dev) - Risk tools for use within the crude and crude products trading space with partial implementation of R's PerformanceAnalytics.
- [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib) - Portfolio Optimization and Quantitative Strategic Asset Allocation in Python.

### Factor Analysis

- [alphalens](https://github.com/quantopian/alphalens) - Performance analysis of predictive alpha factors.
- [Spectre](https://github.com/Heerozh/spectre) - GPU-accelerated Factors analysis library and Backtester

### Time Series

- [ARCH](https://github.com/bashtage/arch) - ARCH models in Python.
- [statsmodels](http://statsmodels.sourceforge.net) - Python module that allows users to explore data, estimate statistical models, and perform statistical tests.
- [dynts](https://github.com/quantmind/dynts) - Python package for timeseries analysis and manipulation.
- [PyFlux](https://github.com/RJT1990/pyflux) - Python library for timeseries modelling and inference (frequentist and Bayesian) on models.
- [tsfresh](https://github.com/blue-yonder/tsfresh) - Automatic extraction of relevant features from time series.
- [hasura/quandl-metabase](https://platform.hasura.io/hub/projects/anirudhm/quandl-metabase-time-series) - Hasura quickstart to visualize Quandl's timeseries datasets with Metabase.
- [Facebook Prophet](https://github.com/facebook/prophet) - Tool for producing high quality forecasts for time series data that has multiple seasonality with linear or non-linear growth.
- [tsmoothie](https://github.com/cerlymarco/tsmoothie) - A python library for time-series smoothing and outlier detection in a vectorized way.
- [pmdarima](https://github.com/alkaline-ml/pmdarima) - A statistical library designed to fill the void in Python's time series analysis capabilities, including the equivalent of R's auto.arima function.
- [gluon-ts](https://github.com/awslabs/gluon-ts) - vProbabilistic time series modeling in Python.

### Calendars

- [exchange_calendars](https://github.com/gerrymanoim/exchange_calendars) - Stock Exchange Trading Calendars.
- [bizdays](https://github.com/wilsonfreitas/python-bizdays) - Business days calculations and utilities.
- [pandas_market_calendars](https://github.com/rsheftel/pandas_market_calendars) - Exchange calendars to use with pandas for trading applications.

### Data Sources

- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo! Finance market data downloader (+faster Pandas Datareader)
- [findatapy](https://github.com/cuemacro/findatapy) - Python library to download market data via Bloomberg, Quandl, Yahoo etc.
- [googlefinance](https://github.com/hongtaocai/googlefinance) - Python module to get real-time stock data from Google Finance API.
- [yahoo-finance](https://github.com/lukaszbanasiak/yahoo-finance) - Python module to get stock data from Yahoo! Finance.
- [pandas-datareader](https://github.com/pydata/pandas-datareader) - Python module to get data from various sources (Google Finance, Yahoo Finance, FRED, OECD, Fama/French, World Bank, Eurostat...) into Pandas datastructures such as DataFrame, Panel with a caching mechanism.
- [pandas-finance](https://github.com/davidastephens/pandas-finance) - High level API for access to and analysis of financial data.
- [pyhoofinance](https://github.com/innes213/pyhoofinance) - Rapidly queries Yahoo Finance for multiple tickers and returns typed data for analysis.
- [yfinanceapi](https://github.com/Karthik005/yfinanceapi) - Finance API for Python.
- [yql-finance](https://github.com/slawek87/yql-finance) - yql-finance is simple and fast. API returns stock closing prices for current period of time and current stock ticker (i.e. APPL, GOOGL).
- [ystockquote](https://github.com/cgoldberg/ystockquote) - Retrieve stock quote data from Yahoo Finance.
- [wallstreet](https://github.com/mcdallas/wallstreet) - Real time stock and option data.
- [stock_extractor](https://github.com/ZachLiuGIS/stock_extractor) - General Purpose Stock Extractors from Online Resources.
- [Stockex](https://github.com/cttn/Stockex) - Python wrapper for Yahoo! Finance API.
- [finsymbols](https://github.com/skillachie/finsymbols) - Obtains stock symbols and relating information for SP500, AMEX, NYSE, and NASDAQ.
- [FRB](https://github.com/avelkoski/FRB) - Python Client for FRED® API.
- [inquisitor](https://github.com/econdb/inquisitor) - Python Interface to Econdb.com API.
- [yfi](https://github.com/nickelkr/yfi) - Yahoo! YQL library.
- [chinesestockapi](https://pypi.org/project/chinesestockapi/) - Python API to get Chinese stock price.
- [exchange](https://github.com/akarat/exchange) - Get current exchange rate.
- [ticks](https://github.com/jamescnowell/ticks) - Simple command line tool to get stock ticker data.
- [pybbg](https://github.com/bpsmith/pybbg) - Python interface to Bloomberg COM APIs.
- [ccy](https://github.com/lsbardel/ccy) - Python module for currencies.
- [tushare](https://pypi.org/project/tushare/) - A utility for crawling historical and Real-time Quotes data of China stocks.
- [jsm](https://pypi.org/project/jsm/) - Get the japanese stock market data.
- [cn_stock_src](https://github.com/jealous/cn_stock_src) - Utility for retrieving basic China stock data from different sources.
- [coinmarketcap](https://github.com/barnumbirr/coinmarketcap) - Python API for coinmarketcap.
- [after-hours](https://github.com/datawrestler/after-hours) - Obtain pre market and after hours stock prices for a given symbol.
- [bronto-python](https://pypi.org/project/bronto-python/) - Bronto API Integration for Python.
- [pytdx](https://github.com/rainx/pytdx) - Python Interface for retrieving chinese stock realtime quote data from TongDaXin Nodes.
- [pdblp](https://github.com/matthewgilbert/pdblp) - A simple interface to integrate pandas and the Bloomberg Open API.
- [tiingo](https://github.com/hydrosquall/tiingo-python) - Python interface for daily composite prices/OHLC/Volume + Real-time News Feeds, powered by the Tiingo Data Platform.
- [iexfinance](https://github.com/addisonlynch/iexfinance) - Python Interface for retrieving real-time and historical prices and equities data from The Investor's Exchange.
- [pyEX](https://github.com/timkpaine/pyEX) - Python interface to IEX with emphasis on pandas, support for streaming data, premium data, points data (economic, rates, commodities), and technical indicators.
- [alpaca-trade-api](https://github.com/alpacahq/alpaca-trade-api-python) - Python interface for retrieving real-time and historical prices from Alpaca API as well as trade execution.
- [metatrader5](https://pypi.org/project/MetaTrader5/) - API Connector to MetaTrader 5 Terminal
- [akshare](https://github.com/jindaxiang/akshare) - AkShare is an elegant and simple financial data interface library for Python, built for human beings! <https://akshare.readthedocs.io>
- [yahooquery](https://github.com/dpguthrie/yahooquery) - Python interface for retrieving data through unofficial Yahoo Finance API.
- [investpy](https://github.com/alvarobartt/investpy) - Financial Data Extraction from Investing.com with Python! <https://investpy.readthedocs.io/>
- [yliveticker](https://github.com/yahoofinancelive/yliveticker) - Live stream of market data from Yahoo Finance websocket.
- [bbgbridge](https://github.com/ran404/bbgbridge) - Easy to use Bloomberg Desktop API wrapper for Python.
- [alpha_vantage](https://github.com/RomelTorres/alpha_vantage) - A python wrapper for Alpha Vantage API for financial data.
- [FinanceDataReader](https://github.com/FinanceData/FinanceDataReader) - Open Source Financial data reader for U.S, Korean, Japanese, Chinese, Vietnamese Stocks
- [pystlouisfed](https://github.com/TomasKoutek/pystlouisfed) - Python client for Federal Reserve Bank of St. Louis API - FRED, ALFRED, GeoFRED and FRASER.
- [python-bcb](https://github.com/wilsonfreitas/python-bcb) - Python interface to Brazilian Central Bank web services.
- [market-prices](https://github.com/maread99/market_prices) - Create meaningful OHLCV datasets from knowledge of [exchange-calendars](https://github.com/gerrymanoim/exchange_calendars) (works out-the-box with data from Yahoo Finance).

### Excel Integration

- [xlwings](https://www.xlwings.org/) - Make Excel fly with Python.
- [openpyxl](https://openpyxl.readthedocs.io/en/latest/) - Read/Write Excel 2007 xlsx/xlsm files.
- [xlrd](https://github.com/python-excel/xlrd) - Library for developers to extract data from Microsoft Excel spreadsheet files.
- [xlsxwriter](https://xlsxwriter.readthedocs.io/) - Write files in the Excel 2007+ XLSX file format.
- [xlwt](https://github.com/python-excel/xlwt) - Library to create spreadsheet files compatible with MS Excel 97/2000/XP/2003 XLS files, on any platform.
- [DataNitro](https://datanitro.com/) - DataNitro also offers full-featured Python-Excel integration, including UDFs. Trial downloads are available, but users must purchase a license.
- [xlloop](http://xlloop.sourceforge.net) - XLLoop is an open source framework for implementing Excel user-defined functions (UDFs) on a centralised server (a function server).
- [expy](http://www.bnikolic.co.uk/expy/expy.html) - The ExPy add-in allows easy use of Python directly from within an Microsoft Excel spreadsheet, both to execute arbitrary code and to define new Excel functions.
- [pyxll](https://www.pyxll.com) - PyXLL is an Excel add-in that enables you to extend Excel using nothing but Python code.

### Visualization

- [D-Tale](https://github.com/man-group/dtale) - Visualizer for pandas dataframes and xarray datasets.
- [mplfinance](https://github.com/matplotlib/mplfinance) - matplotlib utilities for the visualization, and visual analysis, of financial data.
- [finplot](https://github.com/highfestiva/finplot) - Performant and effortless finance plotting for Python.
- [finvizfinance](https://github.com/lit26/finvizfinance) - Finviz analysis python library.

## R

### Numerical Libraries & Data Structures

- [xts](https://github.com/joshuaulrich/xts) - eXtensible Time Series: Provide for uniform handling of R's different time-based data classes by extending zoo, maximizing native format information preservation and allowing for user level customization and extension, while simplifying cross-class interoperability.
- [data.table](https://github.com/Rdatatable/data.table) - Extension of data.frame: Fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins, fast add/modify/delete of columns by group using no copies at all, list columns and a fast file reader (fread). Offers a natural and flexible syntax, for faster development.
- [sparseEigen](https://github.com/dppalomar/sparseEigen) - Sparse pricipal component analysis.
- [TSdbi](http://tsdbi.r-forge.r-project.org/) - Provides a common interface to time series databases.
- [tseries](https://cran.r-project.org/web/packages/tseries/index.html) - Time Series Analysis and Computational Finance.
- [zoo](https://cran.r-project.org/web/packages/zoo/index.html) - S3 Infrastructure for Regular and Irregular Time Series (Z's Ordered Observations).
- [tis](https://cran.r-project.org/web/packages/tis/index.html) - Functions and S3 classes for time indexes and time indexed series, which are compatible with FAME frequencies.
- [tfplot](https://cran.r-project.org/web/packages/tfplot/index.html) - Utilities for simple manipulation and quick plotting of time series data.
- [tframe](https://cran.r-project.org/web/packages/tframe/index.html) - A kernel of functions for programming time series methods in a way that is relatively independently of the representation of time.

### Data Sources

- [IBrokers](https://cran.r-project.org/web/packages/IBrokers/index.html) - Provides native R access to Interactive Brokers Trader Workstation API.
- [Rblpapi](https://github.com/Rblp/Rblpapi) - An R Interface to 'Bloomberg' is provided via the 'Blp API'.
- [Quandl](https://www.quandl.com/tools/r) - Get Financial Data Directly Into R.
- [Rbitcoin](https://github.com/jangorecki/Rbitcoin) - Unified markets API interface (bitstamp, kraken, btce, bitmarket).
- [GetTDData](https://github.com/msperlin/GetTDData) - Downloads and aggregates data for Brazilian government issued bonds directly from the website of Tesouro Direto.
- [GetHFData](https://github.com/msperlin/GetHFData) - Downloads and aggregates high frequency trading data for Brazilian instruments directly from Bovespa ftp site.
- [Reddit WallstreetBets API](https://dashboard.nbshare.io/apps/reddit/api/) - Provides daily top 50 stocks from reddit (subreddit) Wallstreetbets and their sentiments via the API.
- [td](https://github.com/eddelbuettel/td) - Interfaces the 'twelvedata' API for stocks and (digital and standard) currencies.
- [rbcb](https://github.com/wilsonfreitas/rbcb) - R interface to Brazilian Central Bank web services.

### Financial Instruments and Pricing

- [RQuantLib](http://dirk.eddelbuettel.com/code/rquantlib.html) - RQuantLib connects GNU R with QuantLib.
- [quantmod](https://cran.r-project.org/web/packages/quantmod/index.html) - Quantitative Financial Modelling Framework.
- [Rmetrics](https://www.rmetrics.org) - The premier open source software solution for teaching and training quantitative finance.
  - [fAsianOptions](https://cran.r-project.org/web/packages/fAsianOptions/index.html) - EBM and Asian Option Valuation.
  - [fAssets](https://cran.r-project.org/web/packages/fAssets/index.html) - Analysing and Modelling Financial Assets.
  - [fBasics](https://cran.r-project.org/web/packages/fBasics/index.html) - Markets and Basic Statistics.
  - [fBonds](https://cran.r-project.org/web/packages/fBonds/index.html) - Bonds and Interest Rate Models.
  - [fExoticOptions](https://cran.r-project.org/web/packages/fExoticOptions/index.html) - Exotic Option Valuation.
  - [fOptions](https://cran.r-project.org/web/packages/fOptions/index.html) - Pricing and Evaluating Basic Options.
  - [fPortfolio](https://cran.r-project.org/web/packages/fPortfolio/index.html) - Portfolio Selection and Optimization.
- [portfolio](https://github.com/dgerlanc/portfolio) - Analysing equity portfolios.
- [sparseIndexTracking](https://github.com/dppalomar/sparseIndexTracking) - Portfolio design to track an index.
- [covFactorModel](https://github.com/dppalomar/covFactorModel) - Covariance matrix estimation via factor models.
- [riskParityPortfolio](https://github.com/dppalomar/riskParityPortfolio) - Blazingly fast design of risk parity portfolios.
- [sde](https://cran.r-project.org/web/packages/sde/index.html) - Simulation and Inference for Stochastic Differential Equations.
- [YieldCurve](https://cran.r-project.org/web/packages/YieldCurve/index.html) - Modelling and estimation of the yield curve.
- [SmithWilsonYieldCurve](https://cran.r-project.org/web/packages/SmithWilsonYieldCurve/index.html) - Constructs a yield curve by the Smith-Wilson method from a table of LIBOR and SWAP rates.
- [ycinterextra](https://cran.r-project.org/web/packages/ycinterextra/index.html) - Yield curve or zero-coupon prices interpolation and extrapolation.
- [AmericanCallOpt](https://cran.r-project.org/web/packages/AmericanCallOpt/index.html) - This package includes pricing function for selected American call options with underlying assets that generate payouts.
- [VarSwapPrice](https://cran.r-project.org/web/packages/VarSwapPrice/index.html) - Pricing a variance swap on an equity index.
- [RND](https://cran.r-project.org/web/packages/RND/index.html) - Risk Neutral Density Extraction Package.
- [LSMonteCarlo](https://cran.r-project.org/web/packages/LSMonteCarlo/index.html) - American options pricing with Least Squares Monte Carlo method.
- [OptHedging](https://cran.r-project.org/web/packages/OptHedging/index.html) - Estimation of value and hedging strategy of call and put options.
- [tvm](https://cran.r-project.org/web/packages/tvm/index.html) - Time Value of Money Functions.
- [OptionPricing](https://cran.r-project.org/web/packages/OptionPricing/index.html) - Option Pricing with Efficient Simulation Algorithms.
- [credule](https://github.com/blenezet/credule) - Credit Default Swap Functions.
- [derivmkts](https://cran.r-project.org/web/packages/derivmkts/index.html) - Functions and R Code to Accompany Derivatives Markets.
- [FinCal](https://github.com/felixfan/FinCal) - Package for time value of money calculation, time series analysis and computational finance.
- [r-quant](https://github.com/artyyouth/r-quant) - R code for quantitative analysis in finance.
- [options.studies](https://github.com/taylorizing/options.studies) - options trading studies functions for use with options.data package and shiny.
- [PortfolioAnalytics](https://github.com/braverock/PortfolioAnalytics) - Portfolio Analysis, Including Numerical Methods for Optimizationof Portfolios.
- [fmbasics](https://github.com/imanuelcostigan/fmbasics) - Financial Market Building Blocks.
- [R-fixedincome](https://github.com/wilsonfreitas/R-fixedincome) - Fixed income tools for R.

### Trading

- [backtest](https://cran.r-project.org/web/packages/backtest/index.html) - Exploring Portfolio-Based Conjectures About Financial Instruments.
- [pa](https://cran.r-project.org/web/packages/pa/index.html) - Performance Attribution for Equity Portfolios.
- [TTR](https://github.com/joshuaulrich/TTR) - Technical Trading Rules.
- [QuantTools](https://quanttools.bitbucket.io/_site/index.html) - Enhanced Quantitative Trading Modelling.
- [blotter](https://github.com/braverock/blotter) - Transaction infrastructure for defining instruments, transactions, portfolios and accounts for trading systems and simulation. Provides portfolio support for multi-asset class and multi-currency portfolios. Actively maintained and developed.

### Backtesting

- [quantstrat](https://github.com/braverock/quantstrat) - Transaction-oriented infrastructure for constructing trading systems and simulation. Provides support for multi-asset class and multi-currency portfolios for backtesting and other financial research.

### Risk Analysis

- [PerformanceAnalytics](https://github.com/braverock/PerformanceAnalytics) - Econometric tools for performance and risk analysis.

### Factor Analysis

- [FactorAnalytics](https://github.com/braverock/FactorAnalytics) - The FactorAnalytics package contains fitting and analysis methods for the three main types of factor models used in conjunction with portfolio construction, optimization and risk management, namely fundamental factor models, time series factor models and statistical factor models.
- [Expected Returns](https://github.com/JustinMShea/ExpectedReturns) - Solutions for enhancing portfolio diversification and replications of seminal papers with R, most of which are discussed in one of the best investment references of the recent decade, Expected Returns: An Investors Guide to Harvesting Market Rewards by Antti Ilmanen.

### Time Series

- [tseries](https://cran.r-project.org/web/packages/tseries/index.html) - Time Series Analysis and Computational Finance.
- [fGarch](https://cran.r-project.org/web/packages/fGarch/index.html) - Rmetrics - Autoregressive Conditional Heteroskedastic Modelling.
- [timeSeries](https://cran.r-project.org/web/packages/timeSeries/index.html) - Rmetrics - Financial Time Series Objects.
- [rugarch](https://github.com/alexiosg/rugarch) - Univariate GARCH Models.
- [rmgarch](https://github.com/alexiosg/rmgarch) - Multivariate GARCH Models.
- [tidypredict](https://github.com/edgararuiz/tidypredict) - Run predictions inside the database <https://tidypredict.netlify.com/>.
- [tidyquant](https://github.com/business-science/tidyquant) - Bringing financial analysis to the tidyverse.
- [timetk](https://github.com/business-science/timetk) - A toolkit for working with time series in R.
- [tibbletime](https://github.com/business-science/tibbletime) - Built on top of the tidyverse, tibbletime is an extension that allows for the creation of time aware tibbles through the setting of a time index.
- [matrixprofile](https://github.com/matrix-profile-foundation/matrixprofile) - Time series data mining library built on top of the novel Matrix Profile data structure and algorithms.
- [garchmodels](https://github.com/AlbertoAlmuinha/garchmodels) - A parsnip backend for GARCH models.

### Calendars

- [timeDate](https://cran.r-project.org/web/packages/timeDate/index.html) - Chronological and Calendar Objects
- [bizdays](https://github.com/wilsonfreitas/R-bizdays) - Business days calculations and utilities

## Matlab

### FrameWorks

- [QUANTAXIS](https://github.com/yutiansut/quantaxis) - Integrated Quantitative Toolbox with Matlab.

## Julia

- [QuantLib.jl](https://github.com/pazzo83/QuantLib.jl) - Quantlib implementation in pure Julia.
- [Ito.jl](https://github.com/aviks/Ito.jl) - A Julia package for quantitative finance.
- [TALib.jl](https://github.com/femtotrader/TALib.jl) - A Julia wrapper for TA-Lib.
- [Miletus.jl](https://github.com/JuliaComputing/Miletus.jl) - A financial contract definition, modeling language, and valuation framework.
- [Temporal.jl](https://github.com/dysonance/Temporal.jl) - Flexible and efficient time series class & methods.
- [Indicators.jl](https://github.com/dysonance/Indicators.jl) - Financial market technical analysis & indicators on top of Temporal.
- [Strategems.jl](https://github.com/dysonance/Strategems.jl) - Quantitative systematic trading strategy development and backtesting.
- [TimeSeries.jl](https://github.com/JuliaStats/TimeSeries.jl) - Time series toolkit for Julia.
- [MarketTechnicals.jl](https://github.com/JuliaQuant/MarketTechnicals.jl) - Technical analysis of financial time series on top of TimeSeries.
- [MarketData.jl](https://github.com/JuliaQuant/MarketData.jl) - Time series market data.
- [TimeFrames.jl](https://github.com/femtotrader/TimeFrames.jl) - A Julia library that defines TimeFrame (essentially for resampling TimeSeries).

## Java

- [Strata](http://strata.opengamma.io/) - Modern open-source analytics and market risk library designed and written in Java.
- [JQuantLib](http://www.jquantlib.org) - JQuantLib is a free, open-source, comprehensive framework for quantitative finance, written in 100% Java.
- [finmath.net](http://finmath.net) - Java library with algorithms and methodologies related to mathematical finance.
- [quantcomponents](https://github.com/lsgro/quantcomponents) - Free Java components for Quantitative Finance and Algorithmic Trading.
- [DRIP](https://lakshmidrip.github.io/DRIP) - Fixed Income, Asset Allocation, Transaction Cost Analysis, XVA Metrics Libraries.
- [ta4j](https://github.com/ta4j/ta4j) - A Java library for technical analysis.

## JavaScript

- [finance.js](https://github.com/ebradyjobory/finance.js) - A JavaScript library for common financial calculations.
- [portfolio-allocation](https://github.com/lequant40/portfolio_allocation_js) - PortfolioAllocation is a JavaScript library designed to help constructing financial portfolios made of several assets: bonds, commodities, cryptocurrencies, currencies, exchange traded funds (ETFs), mutual funds, stocks...
- [Ghostfolio](https://github.com/ghostfolio/ghostfolio) - Wealth management software to keep track of financial assets like stocks, ETFs or cryptocurrencies and make solid, data-driven investment decisions.
- [IndicatorTS](https://github.com/cinar/indicatorts) - Indicator is a TypeScript module providing various stock technical analysis indicators, strategies, and a backtest framework for trading.
- [ccxt](https://github.com/ccxt/ccxt) - A JavaScript / Python / PHP cryptocurrency trading API with support for more than 100 bitcoin/altcoin exchanges.

### Data Visualization

- [QUANTAXIS_Webkit](https://github.com/yutiansut/QUANTAXIS_Webkit) - An awesome visualization center based on quantaxis.

## Haskell

- [quantfin](https://github.com/boundedvariation/quantfin) - quant finance in pure haskell.
- [hqfl](https://github.com/co-category/hqfl) - Haskell Quantitative Finance Library.
- [Haxcel](https://github.com/MarcusRainbow/Haxcel) - Excel Addin for Haskell.
- [Ffinar](https://github.com/MarcusRainbow/Ffinar) - A financial maths library in Haskell.

## Scala

- [QuantScale](https://github.com/choucrifahed/quantscale) - Scala Quantitative Finance Library.
- [Scala Quant](https://github.com/frankcash/Scala-Quant) - Scala library for working with stock data from IFTTT recipes or Google Finance.

## Ruby

- [Jiji](https://github.com/unageanu/jiji2) - Open Source Forex algorithmic trading framework using OANDA REST API.

## Elixir/Erlang

- [Tai](https://github.com/fremantle-capital/tai) - Open Source composable, real time, market data and trade execution toolkit.
- [Workbench](https://github.com/fremantle-industries/workbench) - From Idea to Execution - Manage your trading operation across a globally distributed cluster
- [Prop](https://github.com/fremantle-industries/prop) - An open and opinionated trading platform using productive & familiar open source libraries and tools for strategy research, execution and operation.

## Golang

- [Kelp](https://github.com/stellar/kelp) - Kelp is an open-source Golang algorithmic cryptocurrency trading bot that runs on centralized exchanges and Stellar DEX (command-line usage and desktop GUI).
- [marketstore](https://github.com/alpacahq/marketstore) - DataFrame Server for Financial Timeseries Data.
- [IndicatorGo](https://github.com/cinar/indicator) - IndicatorGo is a Golang module providing various stock technical analysis indicators, strategies, and a backtest framework for trading.

## CPP

- [TradeFrame](https://github.com/rburkholder/trade-frame) - C++ 17 based framework/library (with sample applications) for testing options based automated trading ideas using DTN IQ real time data feed and Interactive Brokers (TWS API) for trade execution. Comes with built-in [Option Greeks/IV](https://github.com/rburkholder/trade-frame/tree/master/lib/TFOptions) calculation library.

## Frameworks

- [QuantLib](https://www.quantlib.org) - The QuantLib project is aimed at providing a comprehensive software framework for quantitative finance.
  - [JQuantLib](http://www.jquantlib.org) - Java port.
  - [RQuantLib](http://dirk.eddelbuettel.com/code/rquantlib.html) - R port.
  - [QuantLibAddin](https://www.quantlib.org/quantlibaddin/) - Excel support.
  - [QuantLibXL](https://www.quantlib.org/quantlibxl/) - Excel support.
  - [QLNet](https://github.com/amaggiulli/qlnet) - .Net port.
  - [PyQL](https://github.com/enthought/pyql) - Python port.
  - [QuantLib.jl](https://github.com/pazzo83/QuantLib.jl) - Julia port.
- [TA-Lib](https://ta-lib.org) - perform technical analysis of financial market data.
- [Portfolio Optimizer](https://portfoliooptimizer.io/) - Portfolio Optimizer is a Web API for portfolio analysis and optimization.

## CSharp

- [QuantConnect](https://github.com/QuantConnect/Lean) - Lean Engine is an open-source fully managed C# algorithmic trading engine built for desktop and cloud usage.
- [StockSharp](https://github.com/StockSharp/StockSharp) - Algorithmic trading and quantitative trading open source platform to develop trading robots (stock markets, forex, crypto, bitcoins, and options).
- [TDAmeritrade.DotNetCore](https://github.com/NVentimiglia/TDAmeritrade.DotNetCore) - Free, open-source .NET Client for the TD Ameritrade Trading Platform. Helps developers integrate TD Ameritrade API into custom trading solutions.

## Rust

- [QuantMath](https://github.com/MarcusRainbow/QuantMath) - Financial maths library for risk-neutral pricing and risk

## Reproducing Works, Training & Books

- [Derman Papers](https://github.com/MarcosCarreira/DermanPapers) - Notebooks that replicate original quantitative finance papers from Emanuel Derman.
- [ML-Quant](https://www.ml-quant.com/) - Top Quant resources like ArXiv (sanity), SSRN, RePec, Journals, Podcasts, Videos, and Blogs.
- [volatility-trading](https://github.com/jasonstrimpel/volatility-trading) - A complete set of volatility estimators based on Euan Sinclair's Volatility Trading.
- [quant](https://github.com/paulperry/quant) - Quantitative Finance and Algorithmic Trading exhaust; mostly ipython notebooks based on Quantopian, Zipline, or Pandas.
- [fecon235](https://github.com/rsvp/fecon235) - Open source project for software tools in financial economics. Many jupyter notebook to verify theoretical ideas and practical methods interactively.
- [Quantitative-Notebooks](https://github.com/LongOnly/Quantitative-Notebooks) - Educational notebooks on quantitative finance, algorithmic trading, financial modelling and investment strategy
- [QuantEcon](https://quantecon.org/) - Lecture series on economics, finance, econometrics and data science; QuantEcon.py, QuantEcon.jl, notebooks
- [FinanceHub](https://github.com/Finance-Hub/FinanceHub) - Resources for Quantitative Finance
- [Python_Option_Pricing](https://github.com/dedwards25/Python_Option_Pricing) - An libary to price financial options written in Python. Includes: Black Scholes, Black 76, Implied Volatility, American, European, Asian, Spread Options.
- [python-training](https://github.com/jpmorganchase/python-training) - J.P. Morgan's Python training for business analysts and traders.
- [Stock_Analysis_For_Quant](https://github.com/LastAncientOne/Stock_Analysis_For_Quant) - Different Types of Stock Analysis in Excel, Matlab, Power BI, Python, R, and Tableau.
- [algorithmic-trading-with-python](https://github.com/chrisconlan/algorithmic-trading-with-python) - Source code for Algorithmic Trading with Python (2020) by Chris Conlan.
- [MEDIUM_NoteBook](https://github.com/cerlymarco/MEDIUM_NoteBook) - Repository containing notebooks of [cerlymarco](https://github.com/cerlymarco)'s posts on Medium.
- [QuantFinance](https://github.com/PythonCharmers/QuantFinance) - Training materials in quantitative finance.
- [MarketAnalysis](https://github.com/Poseyy/MarketAnalysis) - Implementing many different methods and popular analysis tools in Python.
- [IPythonScripts](https://github.com/mgroncki/IPythonScripts) - Tutorials about Quantitative Finance in Python and QuantLib: Pricing, xVAs, Hedging, Portfolio Optimisation, Machine Learning and Deep Learning.
- [Computational-Finance-Course](https://github.com/LechGrzelak/Computational-Finance-Course) - Materials for the course of Computational Finance.
- [Machine-Learning-for-Asset-Managers](https://github.com/emoen/Machine-Learning-for-Asset-Managers) - Implementation of code snippets, exercises and application to live data from Machine Learning for Asset Managers (Elements in Quantitative Finance) written by Prof. Marcos López de Prado.
- [Python-for-Finance-Cookbook](https://github.com/PacktPublishing/Python-for-Finance-Cookbook) - Python for Finance Cookbook, published by Packt.
- [modelos_vol_derivativos](https://github.com/ysaporito/modelos_vol_derivativos) - "Modelos de Volatilidade para Derivativos" book's Jupyter notebooks
- [NMOF](https://github.com/enricoschumann/NMOF) - Functions, examples and data from the first and the second edition of "Numerical Methods and Optimization in Finance" by M. Gilli, D. Maringer and E. Schumann (2019, ISBN:978-0128150658).
- [py4fi2nd](https://github.com/yhilpisch/py4fi2nd) - Jupyter Notebooks and code for Python for Finance (2nd ed., O'Reilly) by Yves Hilpisch.
- [aiif](https://github.com/yhilpisch/aiif) - Jupyter Notebooks and code for the book Artificial Intelligence in Finance (O'Reilly) by Yves Hilpisch.
- [py4at](https://github.com/yhilpisch/py4at) - Jupyter Notebooks and code for the book Python for Algorithmic Trading (O'Reilly) by Yves Hilpisch.
- [dawp](https://github.com/yhilpisch/dawp) - Jupyter Notebooks and code for Derivatives Analytics with Python (Wiley Finance) by Yves Hilpisch.
- [dx](https://github.com/yhilpisch/dx) - DX Analytics | Financial and Derivatives Analytics with Python.
- [QuantFinanceBook](https://github.com/LechGrzelak/QuantFinanceBook) - Quantitative Finance book.
- [rough_bergomi](https://github.com/ryanmccrickerd/rough_bergomi) - A Python implementation of the rough Bergomi model.
- [frh-fx](https://github.com/ryanmccrickerd/frh-fx) - A python implementation of the fast-reversion Heston model of Mechkov for FX purposes.
- [value-investing-studies](https://github.com/euclidjda/value-investing-studies) - A collection of data analysis studies that examine the performance and characteristics of value investing over long periods of time.
- [machine-learning-asset-management](https://github.com/firmai/machine-learning-asset-management) - Machine Learning in Asset Management (by @firmai).
- [Deep-Learning-Machine-Learning-Stock](https://github.com/LastAncientOne/Deep-Learning-Machine-Learning-Stock) - Deep Learning and Machine Learning stocks represent a promising long-term or short-term opportunity for investors and traders.
- [Technical_Analysis_and_Feature_Engineering](https://github.com/jo-cho/Technical_Analysis_and_Feature_Engineering) - Feature Engineering and Feature Importance of Machine Learning in Financial Market.
- [Differential Machine Learning and Axes that matter by Brian Huge and Antoine Savine](https://github.com/differential-machine-learning/notebooks) - Implement, demonstrate, reproduce and extend the results of the Risk articles 'Differential Machine Learning' (2020) and 'PCA with a Difference' (2021) by Huge and Savine, and cover implementation details left out from the papers.
