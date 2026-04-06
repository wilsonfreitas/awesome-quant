# Awesome Quant

A curated list of insanely awesome libraries, packages and resources for Quants (Quantitative Finance).

[![](https://awesome.re/badge.svg)](https://awesome.re)

## Contents

- [Numerical Libraries & Data Structures](#numerical-libraries-data-structures)
- [Financial Instruments & Pricing](#financial-instruments-pricing)
- [Technical Indicators](#technical-indicators)
- [Trading & Backtesting](#trading-backtesting)
- [Portfolio Optimization & Risk Analysis](#portfolio-optimization-risk-analysis)
- [Factor Analysis](#factor-analysis)
- [Sentiment Analysis & Alternative Data](#sentiment-analysis-alternative-data)
- [Time Series Analysis](#time-series-analysis)
- [Market Data & Data Sources](#market-data-data-sources)
- [Prediction Markets](#prediction-markets)
- [Calendars & Market Hours](#calendars-market-hours)
- [Visualization](#visualization)
- [Excel & Spreadsheet Integration](#excel-spreadsheet-integration)
- [Quant Research Environments](#quant-research-environments)
- [Cross-Language Frameworks](#cross-language-frameworks)
- [Reproducing Works, Training & Books](#reproducing-works-training-books)
- [Commercial & Proprietary Services](#commercial-proprietary-services)
- [Related Lists](#related-lists)

## Numerical Libraries & Data Structures

- [numpy](https://www.numpy.org) - `Python` - NumPy is the fundamental package for scientific computing with Python. [GitHub](https://github.com/numpy/numpy)
- [scipy](https://www.scipy.org) - `Python` - SciPy (pronounced “Sigh Pie”) is a Python-based ecosystem of open-source software for mathematics, science, and engineering. [GitHub](https://github.com/scipy/scipy)
- [pandas](https://pandas.pydata.org) - `Python` - pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language. [GitHub](https://github.com/pandas-dev/pandas)
- [polars](https://docs.pola.rs/) - `Python` - Polars is a blazingly fast DataFrame library for manipulating structured data. [GitHub](https://github.com/pola-rs/polars)
- [quantdsl](https://github.com/johnbywater/quantdsl) - `Python` - Domain specific language for quantitative analytics in finance and trading.
- [statistics](https://docs.python.org/3/library/statistics.html) - `Python` - Builtin Python library for all basic statistical calculations.
- [sympy](https://www.sympy.org/) - `Python` - SymPy is a Python library for symbolic mathematics. [GitHub](https://github.com/sympy/sympy)
- [pymc3](https://docs.pymc.io/) - `Python` - Probabilistic Programming in Python: Bayesian Modeling and Probabilistic Machine Learning with Theano. [GitHub](https://github.com/pymc-devs/pymc)
- [modelx](https://docs.modelx.io/) - `Python` - Python reimagination of spreadsheets as formula-centric objects that are interoperable with pandas. [GitHub](https://github.com/fumitoh/modelx)
- [ArcticDB](https://github.com/man-group/ArcticDB) - `Python` - High performance datastore for time series and tick data.
- [CRNG](https://github.com/brotto/crng) - `Python` - Contingency Random Number Generator that produces random numbers with real financial market statistical signatures (fat tails, volatility clustering, kurtosis). Matches 86% of real market metrics vs 14% for NumPy.
- [xts](https://github.com/joshuaulrich/xts) - `R` - eXtensible Time Series: Provide for uniform handling of R's different time-based data classes by extending zoo, maximizing native format information preservation and allowing for user level customization and extension, while simplifying cross-class interoperability.
- [data.table](https://github.com/Rdatatable/data.table) - `R` - Extension of data.frame: Fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins, fast add/modify/delete of columns by group using no copies at all, list columns and a fast file reader (fread). Offers a natural and flexible syntax, for faster development.
- [sparseEigen](https://github.com/dppalomar/sparseEigen) - `R` - Sparse principal component analysis.
- [TSdbi](http://tsdbi.r-forge.r-project.org/) - `R` - Provides a common interface to time series databases.
- [tseries](https://cran.r-project.org/web/packages/tseries/index.html) - `R` - Time Series Analysis and Computational Finance.
- [zoo](https://cran.r-project.org/web/packages/zoo/index.html) - `R` - S3 Infrastructure for Regular and Irregular Time Series (Z's Ordered Observations).
- [tis](https://cran.r-project.org/web/packages/tis/index.html) - `R` - Functions and S3 classes for time indexes and time indexed series, which are compatible with FAME frequencies.
- [tfplot](https://cran.r-project.org/web/packages/tfplot/index.html) - `R` - Utilities for simple manipulation and quick plotting of time series data.
- [tframe](https://cran.r-project.org/web/packages/tframe/index.html) - `R` - A kernel of functions for programming time series methods in a way that is relatively independently of the representation of time.
- [Temporal.jl](https://github.com/dysonance/Temporal.jl) - `Julia` - Flexible and efficient time series class & methods.
- [DataFrames.jl](https://github.com/JuliaData/DataFrames.jl) - `Julia` - In-memory tabular data in Julia.
- [TSFrames.jl](https://github.com/xKDR/TSFrames.jl) - `Julia` - Handle timeseries data on top of the powerful and mature DataFrames.jl.
- [TimeArrays.jl](https://github.com/bhftbootcamp/TimeArrays.jl) - `Julia` - Time series handling for Julia.

## Financial Instruments & Pricing

- [PyQL](https://github.com/enthought/pyql) - `Python` - QuantLib's Python port.
- [pyfin](https://github.com/opendoor-labs/pyfin) - `Python` - Basic options pricing in Python. *ARCHIVED*.
- [vollib](https://github.com/vollib/vollib) - `Python` - vollib is a python library for calculating option prices, implied volatility and greeks.
- [QuantPy](https://github.com/jsmidt/QuantPy) - `Python` - A framework for quantitative finance In python.
- [Finance-Python](https://github.com/alpha-miner/Finance-Python) - `Python` - Python tools for Finance.
- [ffn](https://github.com/pmorissette/ffn) - `Python` - A financial function library for Python.
- [pynance](https://github.com/GriffinAustin/pynance) - `Python` - Lightweight Python library for assembling and analyzing financial data.
- [tia](https://github.com/bpsmith/tia) - `Python` - Toolkit for integration and analysis.
- [pysabr](https://github.com/ynouri/pysabr) - `Python` - SABR model Python implementation.
- [FinancePy](https://github.com/domokane/FinancePy) - `Python` - A Python Finance Library that focuses on the pricing and risk-management of Financial Derivatives, including fixed-income, equity, FX and credit derivatives.
- [gs-quant](https://github.com/goldmansachs/gs-quant) - `Python` - Python toolkit for quantitative finance.
- [willowtree](https://github.com/federicomariamassari/willowtree) - `Python` - Robust and flexible Python implementation of the willow tree lattice for derivatives pricing.
- [financial-engineering](https://github.com/federicomariamassari/financial-engineering) - `Python` - Applications of Monte Carlo methods to financial engineering projects, in Python.
- [optlib](https://github.com/dbrojas/optlib) - `Python` - A library for financial options pricing written in Python.
- [tf-quant-finance](https://github.com/google/tf-quant-finance) - `Python` - High-performance TensorFlow library for quantitative finance.
- [Q-Fin](https://github.com/RomanMichaelPaolucci/Q-Fin) - `Python` - A Python library for mathematical finance.
- [Quantsbin](https://github.com/quantsbin/Quantsbin) - `Python` - Tools for pricing and plotting of vanilla option prices, greeks and various other analysis around them.
- [finoptions](https://github.com/bbcho/finoptions-dev) - `Python` - Complete python implementation of R package fOptions with partial implementation of fExoticOptions for pricing various options.
- [pypme](https://github.com/ymyke/pypme) - `Python` - PME (Public Market Equivalent) calculation.
- [AbsBox](https://github.com/yellowbean/AbsBox) - `Python` - A Python based library to model cashflow for structured product like Asset-backed securities (ABS) and Mortgage-backed securities (MBS).
- [Intrinsic-Value-Calculator](https://github.com/akashaero/Intrinsic-Value-Calculator) - `Python` - A Python tool for quick calculations of a stock's fair value using Discounted Cash Flow analysis.
- [Kelly-Criterion](https://github.com/deltaray-io/kelly-criterion) - `Python` - Kelly Criterion implemented in Python to size portfolios based on J. L. Kelly Jr's formula.
- [rateslib](https://github.com/attack68/rateslib) - `Python` - A fixed income library for pricing bonds and bond futures, and derivatives such as IRS, cross-currency and FX swaps.
- [fypy](https://github.com/jkirkby3/fypy) - `Python` - Vanilla and exotic option pricing library to support quantitative R&D. Focus on pricing interesting/useful models and contracts (including and beyond Black-Scholes), as well as calibration of financial models to market data.
- [Pyderivatives](https://github.com/Julian-Beatty/Pyderivatives) - `Python` - Toolkit for option pricing, implied volatility surfaces, risk-neutral densities, and pricing kernel surfaces with support for advanced models including Heston, Kou, and Bates.
- [quantra](https://github.com/joseprupi/quantraserver) - `Python` - High-performance pricing engine built on QuantLib. It exposes QuantLib's functionality through gRPC and REST APIs, enabling distributed computations with FlatBuffers serialization.
- [optionlab](https://github.com/rgaveiga/optionlab) - `Python` - A Python library for evaluating option trading strategies.
- [flashalpha](https://github.com/FlashAlpha-lab/flashalpha-python) - `Python` - Python client for the FlashAlpha options analytics API.
- [RQuantLib](https://github.com/eddelbuettel/rquantlib) - `R` - RQuantLib connects GNU R with QuantLib.
- [quantmod](https://cran.r-project.org/web/packages/quantmod/index.html) - `R` - Quantitative Financial Modelling Framework. [GitHub](https://github.com/joshuaulrich/quantmod)
- [Rmetrics](https://www.rmetrics.org) - `R` - The premier open source software solution for teaching and training quantitative finance.
  - [fAsianOptions](https://cran.r-project.org/web/packages/fAsianOptions/index.html) - EBM and Asian Option Valuation.
  - [fAssets](https://cran.r-project.org/web/packages/fAssets/index.html) - Analysing and Modelling Financial Assets.
  - [fBasics](https://cran.r-project.org/web/packages/fBasics/index.html) - Markets and Basic Statistics.
  - [fBonds](https://cran.r-project.org/web/packages/fBonds/index.html) - Bonds and Interest Rate Models.
  - [fExoticOptions](https://cran.r-project.org/web/packages/fExoticOptions/index.html) - Exotic Option Valuation.
  - [fOptions](https://cran.r-project.org/web/packages/fOptions/index.html) - Pricing and Evaluating Basic Options.
  - [fPortfolio](https://cran.r-project.org/web/packages/fPortfolio/index.html) - Portfolio Selection and Optimization.
- [sde](https://cran.r-project.org/web/packages/sde/index.html) - `R` - Simulation and Inference for Stochastic Differential Equations.
- [YieldCurve](https://cran.r-project.org/web/packages/YieldCurve/index.html) - `R` - Modelling and estimation of the yield curve.
- [SmithWilsonYieldCurve](https://cran.r-project.org/web/packages/SmithWilsonYieldCurve/index.html) - `R` - Constructs a yield curve by the Smith-Wilson method from a table of LIBOR and SWAP rates.
- [ycinterextra](https://cran.r-project.org/web/packages/ycinterextra/index.html) - `R` - Yield curve or zero-coupon prices interpolation and extrapolation.
- [AmericanCallOpt](https://cran.r-project.org/web/packages/AmericanCallOpt/index.html) - `R` - This package includes pricing function for selected American call options with underlying assets that generate payouts.
- [VarSwapPrice](https://cran.r-project.org/web/packages/VarSwapPrice/index.html) - `R` - Pricing a variance swap on an equity index.
- [RND](https://cran.r-project.org/web/packages/RND/index.html) - `R` - Risk Neutral Density Extraction Package.
- [LSMonteCarlo](https://cran.r-project.org/web/packages/LSMonteCarlo/index.html) - `R` - American options pricing with Least Squares Monte Carlo method.
- [OptHedging](https://cran.r-project.org/web/packages/OptHedging/index.html) - `R` - Estimation of value and hedging strategy of call and put options.
- [tvm](https://cran.r-project.org/web/packages/tvm/index.html) - `R` - Time Value of Money Functions.
- [OptionPricing](https://cran.r-project.org/web/packages/OptionPricing/index.html) - `R` - Option Pricing with Efficient Simulation Algorithms.
- [credule](https://github.com/blenezet/credule) - `R` - Credit Default Swap Functions.
- [derivmkts](https://cran.r-project.org/web/packages/derivmkts/index.html) - `R` - Functions and R Code to Accompany Derivatives Markets. [GitHub](https://github.com/rmcd1024/derivmkts)
- [FinCal](https://github.com/felixfan/FinCal) - `R` - Package for time value of money calculation, time series analysis and computational finance.
- [r-quant](https://github.com/artyyouth/r-quant) - `R` - R code for quantitative analysis in finance.
- [options.studies](https://github.com/taylorizing/options.studies) - `R` - options trading studies functions for use with options.data package and shiny.
- [fmbasics](https://github.com/imanuelcostigan/fmbasics) - `R` - Financial Market Building Blocks.
- [R-fixedincome](https://github.com/wilsonfreitas/R-fixedincome) - `R` - Fixed income tools for R.
- [QuantLib.jl](https://github.com/pazzo83/QuantLib.jl) - `Julia` - Quantlib implementation in pure Julia.
- [Ito.jl](https://github.com/aviks/Ito.jl) - `Julia` - A Julia package for quantitative finance.
- [Miletus.jl](https://github.com/JuliaComputing/Miletus.jl) - `Julia` - A financial contract definition, modeling language, and valuation framework.
- [Strata](http://strata.opengamma.io/) - `Java` - Modern open-source analytics and market risk library designed and written in Java. [GitHub](https://github.com/OpenGamma/Strata)
- [JQuantLib](https://github.com/frgomes/jquantlib) - `Java` - JQuantLib is a free, open-source, comprehensive framework for quantitative finance, written in 100% Java.
- [finmath.net](http://finmath.net) - `Java` - Java library with algorithms and methodologies related to mathematical finance. [GitHub](https://github.com/finmath/finmath-lib)
- [quantcomponents](https://github.com/lsgro/quantcomponents) - `Java` - Free Java components for Quantitative Finance and Algorithmic Trading.
- [DRIP](https://lakshmidrip.github.io/DRIP) - `Java` - Fixed Income, Asset Allocation, Transaction Cost Analysis, XVA Metrics Libraries.
- [finance.js](https://github.com/ebradyjobory/finance.js) - `JavaScript` - A JavaScript library for common financial calculations.
- [quantfin](https://github.com/boundedvariation/quantfin) - `Haskell` - quant finance in pure haskell.
- [Haxcel](https://github.com/MarcusRainbow/Haxcel) - `Haskell` - Excel Addin for Haskell.
- [Ffinar](https://github.com/MarcusRainbow/Ffinar) - `Haskell` - A financial maths library in Haskell.
- [QuantScale](https://github.com/choucrifahed/quantscale) - `Scala` - Scala Quantitative Finance Library.
- [Scala Quant](https://github.com/frankcash/Scala-Quant) - `Scala` - Scala library for working with stock data from IFTTT recipes or Google Finance.
- [QuantMath](https://github.com/MarcusRainbow/QuantMath) - `Rust` - Financial maths library for risk-neutral pricing and risk.
- [RustQuant](https://github.com/avhz/RustQuant) - `Rust` - Quantitative finance library written in Rust.

## Technical Indicators

- [pandas_talib](https://github.com/femtotrader/pandas_talib) - `Python` - A Python Pandas implementation of technical analysis indicators.
- [finta](https://github.com/peerchemist/finta) - `Python` - Common financial technical analysis indicators implemented in Pandas.
- [Tulipy](https://github.com/cirla/tulipy) - `Python` - Financial Technical Analysis Indicator Library (Python bindings for [tulipindicators](https://github.com/TulipCharts/tulipindicators)).
- [lppls](https://github.com/Boulder-Investment-Technologies/lppls) - `Python` - A Python module for fitting the [Log-Periodic Power Law Singularity (LPPLS)](https://en.wikipedia.org/wiki/Didier_Sornette#The_JLS_and_LPPLS_models) model.
- [talipp](https://github.com/nardew/talipp) - `Python` - Incremental technical analysis library for Python.
- [streaming_indicators](https://github.com/mr-easy/streaming_indicators) - `Python` - A python library for computing technical analysis indicators on streaming data.
- [TA-Lib](https://github.com/mrjbq7/ta-lib) - `Python` - Python wrapper for TA-Lib (<http://ta-lib.org/>).
- [ta](https://github.com/bukosabino/ta) - `Python` - Technical Analysis Library using Pandas (Python).
- [bta-lib](https://github.com/mementum/bta-lib) - `Python` - Technical Analysis library in pandas for backtesting algotrading and quantitative analysis.
- [TuneTA](https://github.com/jmrichardson/tuneta) - `Python` - TuneTA optimizes technical indicators using a distance correlation measure to a user defined target feature such as next day return.
- [TTR](https://github.com/joshuaulrich/TTR) - `R` - Technical Trading Rules.
- [TALib.jl](https://github.com/femtotrader/TALib.jl) - `Julia` - A Julia wrapper for TA-Lib.
- [Indicators.jl](https://github.com/dysonance/Indicators.jl) - `Julia` - Financial market technical analysis & indicators on top of Temporal.
- [TechnicalIndicatorCharts.jl](https://github.com/g-gundam/TechnicalIndicatorCharts.jl) - `Julia` - Visualize OnlineTechnicalIndicators.jl using LightweightCharts.jl.
- [MarketTechnicals.jl](https://github.com/JuliaQuant/MarketTechnicals.jl) - `Julia` - Technical analysis of financial time series on top of TimeSeries.
- [OnlineTechnicalIndicators.jl](https://github.com/femtotrader/OnlineTechnicalIndicators.jl) - `Julia` - Julia Technical Analysis Indicators via online algorithms.
- [ta4j](https://github.com/ta4j/ta4j) - `Java` - A Java library for technical analysis.
- [IndicatorTS](https://github.com/cinar/indicatorts) - `JavaScript` - Indicator is a TypeScript module providing various stock technical analysis indicators, strategies, and a backtest framework for trading.
- [chart-patterns](https://github.com/focus1691/chart-patterns) - `JavaScript` - Technical analysis library for Market Profile, Volume Profile, Stacked Imbalances and High Volume Node indicators.
- [orderflow](https://github.com/focus1691/orderflow) - `JavaScript` - Orderflow trade aggregator for building Footprint Candles from exchange websocket data.
- [IndicatorGo](https://github.com/cinar/indicator) - `Golang` - IndicatorGo is a Golang module providing various stock technical analysis indicators, strategies, and a backtest framework for trading.
- [TradeAggregation](https://github.com/MathisWellmann/trade_aggregation-rs) - `Rust` - Aggregate trades into user-defined candles using information driven rules.
- [SlidingFeatures](https://github.com/MathisWellmann/sliding_features-rs) - `Rust` - Chainable tree-like sliding windows for signal processing and technical analysis.
- [fin-primitives](https://github.com/Mattbusel/fin-primitives) - `Rust` - Financial market primitives in Rust: Price/Quantity/Symbol newtypes, BTreeMap order book, OHLCV aggregation, SMA/EMA/RSI indicators, position ledger with PnL, and composable risk monitor.

## Trading & Backtesting

- [AI Quant Agents](https://github.com/demandai/ai-quant-agents) - `Python` - Multi-agent LLM trading analysis where 12 AI agents (analysts, debaters, risk manager) debate stock picks in real-time, supporting US equities and China A-shares.
- [TradeSight](https://github.com/rmbell09-lang/tradesight) - `Python` - AI-powered trading intelligence platform with paper trading, strategy optimization tournaments, 15+ technical indicators, and multi-market scanning.
- [the0](https://github.com/alexanderwanyoike/the0) - `Python` - Self-hosted execution engine for algorithmic trading bots. Write strategies in Python, TypeScript, Rust, C++, C#, Scala, or Haskell and deploy with one command. Each bot runs in an isolated container with scheduled or streaming execution.
- [Investing algorithm framework](https://github.com/coding-kitties/investing-algorithm-framework) - `Python` - Framework for developing, backtesting, and deploying automated trading algorithms.
- [QSTrader](https://github.com/mhallsmoore/qstrader) - `Python` - QSTrader backtesting simulation engine.
- [Blankly](https://github.com/Blankly-Finance/Blankly) - `Python` - Fully integrated backtesting, paper trading, and live deployment.
- [zipline](https://github.com/quantopian/zipline) - `Python` - Pythonic algorithmic trading library.
- [zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded) - `Python` - Zipline, a Pythonic Algorithmic Trading Library.
- [QuantSoftware Toolkit](https://github.com/QuantSoftware/QuantSoftwareToolkit) - `Python` - Python-based open source software framework designed to support portfolio construction and management.
- [quantitative](https://github.com/jeffrey-liang/quantitative) - `Python` - Quantitative finance, and backtesting library.
- [analyzer](https://github.com/llazzaro/analyzer) - `Python` - Python framework for real-time financial and backtesting trading strategies.
- [bt](https://github.com/pmorissette/bt) - `Python` - Flexible Backtesting for Python.
- [backtrader](https://github.com/backtrader/backtrader) - `Python` - Python Backtesting library for trading strategies.
- [pythalesians](https://github.com/thalesians/pythalesians) - `Python` - Python library to backtest trading strategies, plot charts, seamlessly download market data, analyze market patterns etc.
- [pybacktest](https://github.com/ematvey/pybacktest) - `Python` - Vectorized backtesting framework in Python / pandas, designed to make your backtesting easier.
- [pyalgotrade](https://github.com/gbeced/pyalgotrade) - `Python` - Python Algorithmic Trading Library.
- [basana](https://github.com/gbeced/basana) - `Python` - A Python async and event driven framework for algorithmic trading, with a focus on crypto currencies.
- [algobroker](https://github.com/joequant/algobroker) - `Python` - This is an execution engine for algo trading.
- [finmarketpy](https://github.com/cuemacro/finmarketpy) - `Python` - Python library for backtesting trading strategies and analyzing financial markets.
- [binary-martingale](https://github.com/metaperl/binary-martingale) - `Python` - Computer program to automatically trade binary options martingale style.
- [fooltrader](https://github.com/foolcage/fooltrader) - `Python` - the project using big-data technology to provide an uniform way to analyze the whole market.
- [zvt](https://github.com/zvtvz/zvt) - `Python` - the project using sql, pandas to provide an uniform and extendable way to record data, computing factors, select securities, backtesting, realtime trading and it could show all of them in clearly charts in realtime.
- [pylivetrader](https://github.com/alpacahq/pylivetrader) - `Python` - zipline-compatible live trading library.
- [pipeline-live](https://github.com/alpacahq/pipeline-live) - `Python` - zipline's pipeline capability with IEX for live trading.
- [zipline-extensions](https://github.com/quantrocket-llc/zipline-extensions) - `Python` - Zipline extensions and adapters for QuantRocket.
- [moonshot](https://github.com/quantrocket-llc/moonshot) - `Python` - Vectorized backtester and trading engine for QuantRocket based on Pandas.
- [pyqstrat](https://github.com/abbass2/pyqstrat) - `Python` - A fast, extensible, transparent python library for backtesting quantitative strategies.
- [NowTrade](https://github.com/edouardpoitras/NowTrade) - `Python` - Python library for backtesting technical/mechanical strategies in the stock and currency markets.
- [pinkfish](https://github.com/fja05680/pinkfish) - `Python` - A backtester and spreadsheet library for security analysis.
- [PRISM-INSIGHT](https://github.com/dragon1086/prism-insight) - `Python` - AI-powered stock analysis system with 13 specialized agents, automated trading via KIS API, supporting Korean & US markets.
- [FinClaw](https://github.com/NeuZhou/finclaw) - `Python` - AI-powered financial intelligence engine with 8 master strategies across US, CN, and HK markets. Multi-agent architecture with +29.1% annual alpha. 227 tests.
- [aat](https://github.com/timkpaine/aat) - `Python` - Async Algorithmic Trading Engine.
- [Backtesting.py](https://kernc.github.io/backtesting.py/) - `Python` - Backtest trading strategies in Python.
- [catalyst](https://github.com/enigmampc/catalyst) - `Python` - An Algorithmic Trading Library for Crypto-Assets in Python.
- [quantstats](https://github.com/ranaroussi/quantstats) - `Python` - Portfolio analytics for quants, written in Python.
- [jquantstats](https://github.com/Jebel-Quant/jquantstats) - `Python` - Modern variation of quantstats, with additional features and performance improvements.
- [qtpylib](https://github.com/ranaroussi/qtpylib) - `Python` - QTPyLib, Pythonic Algorithmic Trading <http://qtpylib.io>.
- [Quantdom](https://github.com/constverum/Quantdom) - `Python` - Python-based framework for backtesting trading strategies & analyzing financial markets [GUI :neckbeard:.]
- [freqtrade](https://github.com/freqtrade/freqtrade) - `Python` - Free, open source crypto trading bot.
- [algorithmic-trading-with-python](https://github.com/chrisconlan/algorithmic-trading-with-python) - `Python` - Free `pandas` and `scikit-learn` resources for trading simulation, backtesting, and machine learning on financial data.
- [Qlib](https://github.com/microsoft/qlib) - `Python` - An AI-oriented Quantitative Investment Platform by Microsoft. Full ML pipeline of data processing, model training, back-testing; and covers the entire chain of quantitative investment: alpha seeking, risk modeling, portfolio optimization, and order execution.
- [machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) - `Python` - Code and resources for Machine Learning for Algorithmic Trading.
- [AlphaPy](https://github.com/ScottfreeLLC/AlphaPy) - `Python` - Automated Machine Learning [AutoML] with Python, scikit-learn, Keras, XGBoost, LightGBM, and CatBoost.
- [jesse](https://github.com/jesse-ai/jesse) - `Python` - An advanced crypto trading bot written in Python.
- [rqalpha](https://github.com/ricequant/rqalpha) - `Python` - A extendable, replaceable Python algorithmic backtest && trading framework supporting multiple securities.
- [FinRL-Library](https://github.com/AI4Finance-LLC/FinRL-Library) - `Python` - A Deep Reinforcement Learning Library for Automated Trading in Quantitative Finance. NeurIPS 2020.
- [bulbea](https://github.com/achillesrasquinha/bulbea) - `Python` - Deep Learning based Python Library for Stock Market Prediction and Modelling.
- [ib_nope](https://github.com/ajhpark/ib_nope) - `Python` - Automated trading system for NOPE strategy over IBKR TWS.
- [OctoBot](https://github.com/Drakkar-Software/OctoBot) - `Python` - Open source cryptocurrency trading bot for high frequency, arbitrage, TA and social trading with an advanced web interface.
- [OpenFinClaw](https://github.com/cryptoSUN2049/openFinclaw) - `Python` `Rust` - AI-native hedge fund platform: natural language strategy generation, Rust backtesting engine, multi-market execution, and self-evolving strategy pipeline with community leaderboard.
- [Stock-Prediction-Models](https://github.com/huseinzol05/Stock-Prediction-Models) - `Python` - Gathers machine learning and deep learning models for Stock forecasting including trading bots and simulations.
- [AutoTrader](https://github.com/kieran-mackle/AutoTrader) - `Python` - A Python-based development platform for automated trading systems - from backtesting to optimization to livetrading.
- [fast-trade](https://github.com/jrmeier/fast-trade) - `Python` - A library built with backtest portability and performance in mind for backtest trading strategies.
- [qf-lib](https://github.com/quarkfin/qf-lib) - `Python` - QF-Lib is a Python library that provides high quality tools for quantitative finance.
- [tda-api](https://github.com/alexgolec/tda-api) - `Python` - Gather data and trade equities, options, and ETFs via TDAmeritrade.
- [vectorbt](https://github.com/polakowo/vectorbt) - `Python` - Find your trading edge, using a powerful toolkit for backtesting, algorithmic trading, and research.
- [Lean](https://github.com/QuantConnect/Lean) - `Python` `C#` - Lean Algorithmic Trading Engine by QuantConnect (Python, C#).
- [pysystemtrade](https://github.com/robcarver17/pysystemtrade) - `Python` - pysystemtrade is the open source version of Robert Carver's backtesting and trading engine that implements systems according to the framework outlined in his book "Systematic Trading", which is further developed on his [blog](https://qoppac.blogspot.com/).
- [pytrendseries](https://github.com/rafa-rod/pytrendseries) - `Python` - Detect trend in time series, drawdown, drawdown within a constant look-back window , maximum drawdown, time underwater.
- [PyLOB](https://github.com/DrAshBooth/PyLOB) - `Python` - Fully functioning fast Limit Order Book written in Python.
- [PyBroker](https://github.com/edtechre/pybroker) - `Python` - Algorithmic Trading with Machine Learning.
- [OctoBot Script](https://github.com/Drakkar-Software/OctoBot-Script) - `Python` - A quant framework to create cryptocurrencies strategies - from backtesting to optimization to livetrading.
- [hftbacktest](https://github.com/nkaz001/hftbacktest) - `Python` - A high-frequency trading and market-making backtesting tool accounts for limit orders, queue positions, and latencies, utilizing full tick data for trades and order books.
- [vnpy](https://github.com/vnpy/vnpy) - `Python` - VeighNa is a Python-based open source quantitative trading system development framework.
- [Intelligent Trading Bot](https://github.com/asavinov/intelligent-trading-bot) - `Python` - Automatically generating signals and trading based on machine learning and feature engineering.
- [fastquant](https://github.com/enzoampil/fastquant) - `Python` - fastquant allows you to easily backtest investment strategies with as few as 3 lines of python code.
- [nautilus_trader](https://github.com/nautechsystems/nautilus_trader) - `Python` `Rust` - A high-performance algorithmic trading platform and event-driven backtester.
- [YABTE](https://github.com/bsdz/yabte) - `Python` - Yet Another (Python) BackTesting Engine.
- [Trading Strategy](https://github.com/tradingstrategy-ai/getting-started) - `Python` - TradingStrategy.ai is a market data, backtesting, live trading and investor management framework for decentralised finance.
- [Hikyuu](https://github.com/fasiondog/hikyuu) - `Python` `C++` - A base on Python/C++ open source high-performance quant framework for faster analysis and backtesting, contains the complete trading system components for reuse and combination.
- [rust_bt](https://github.com/jensnesten/rust_bt) - `Python` - A high performance, low-latency backtesting engine for testing quantitative trading strategies on historical and live data in Rust.
- [Gunbot Quant](https://github.com/GuntharDeNiro/gunbot-quant) - `Python` - Toolkit for quantitative trading analysis. It integrates an advanced market screener, a multi-strategy, multi-asset backtesting engine. Use with built-in GUI or through CLI.
- [StrateQueue](https://github.com/StrateQueue/StrateQueue) - `Python` - An open‑source, broker‑agnostic Python library that lets you seamlessly deploy strategies from any major backtesting engine to live (or paper) trading with zero code changes and built‑in safety controls.
- [PythonTradingFramework](https://github.com/JustinGuese/python_tradingbot_framework) - `Python` - Python algorithmic trading bot framework for Kubernetes: backtesting, hyperparameter optimization, 150+ technical analysis indicators (RSI, MACD, Bollinger Bands, ADX), portfolio management, PostgreSQL integration, Helm deployment, CronJob scheduling. Minimal overhead, production-ready, Yahoo Finance data.
- [QTradeX-AI-Agents](https://github.com/squidKid-deluxe/QTradeX-AI-Agents) - `Python` - Example strategies for the QTradeX platfrom.
- [QTradeX-Algo-Trading-SDK](https://github.com/squidKid-deluxe/QTradeX-Algo-Trading-SDK) - `Python` - AI-powered SDK featuring algorithmic trading, backtesting, deployment on 100+ exchanges, and multiple optimization engines.
- [antback](https://github.com/ts-kontakt/antback) - `Python` - A lightweight, event-loop-style backtest engine that allows a function-driven imperative style using efficient stateful helper functions and data containers.
- [VARRD](https://github.com/augiemazza/varrd) - `Python` - AI-powered trading edge discovery platform that validates trading ideas with event studies, statistical tests, and real market data. Web app, MCP server, CLI (`pip install varrd`), and Python SDK.
- [JIT-Optimization-Engine](https://github.com/cloudsealed/JIT-Optimization-Engine) - `Python` - High-performance analytical core using LLVM JIT (Numba) to process large-scale telemetry for quant diagnostics.
- [backtest](https://cran.r-project.org/web/packages/backtest/index.html) - `R` - Exploring Portfolio-Based Conjectures About Financial Instruments.
- [pa](https://cran.r-project.org/web/packages/pa/index.html) - `R` - Performance Attribution for Equity Portfolios.
- [QuantTools](https://quanttools.bitbucket.io/_site/index.html) - `R` - Enhanced Quantitative Trading Modelling.
- [blotter](https://github.com/braverock/blotter) - `R` - Transaction infrastructure for defining instruments, transactions, portfolios and accounts for trading systems and simulation. Provides portfolio support for multi-asset class and multi-currency portfolios. Actively maintained and developed.
- [quantstrat](https://github.com/braverock/quantstrat) - `R` - Transaction-oriented infrastructure for constructing trading systems and simulation. Provides support for multi-asset class and multi-currency portfolios for backtesting and other financial research.
- [QUANTAXIS](https://github.com/yutiansut/quantaxis) - `Matlab` - Integrated Quantitative Toolbox with Matlab.
- [PROJ_Option_Pricing_Matlab](https://github.com/jkirkby3/PROJ_Option_Pricing_Matlab) - `Matlab` - Quant Option Pricing - Exotic/Vanilla: Barrier, Asian, European, American, Parisian, Lookback, Cliquet, Variance Swap, Swing, Forward Starting, Step, Fader.
- [Fastback.jl](https://github.com/rbeeli/Fastback.jl) - `Julia` - Blazing fast Julia backtester.
- [Lucky.jl](https://github.com/oliviermilla/Lucky.jl) - `Julia` - Modular, asynchronous trading engine in pure Julia.
- [Strategems.jl](https://github.com/dysonance/Strategems.jl) - `Julia` - Quantitative systematic trading strategy development and backtesting.
- [ccxt](https://github.com/ccxt/ccxt) - `JavaScript` `Python` `PHP` - A JavaScript / Python / PHP cryptocurrency trading API with support for more than 100 bitcoin/altcoin exchanges.
- [TradeClaw](https://github.com/naimkatiman/tradeclaw) - `JavaScript` - Open-source AI trading signal platform with RSI/MACD/EMA confluence scoring, real-time signals for 10+ assets, self-hostable with one Docker command.
- [Jiji](https://github.com/unageanu/jiji2) - `Ruby` - Open Source Forex algorithmic trading framework using OANDA REST API.
- [Tai](https://github.com/fremantle-capital/tai) - `Elixir/Erlang` - Open Source composable, real time, market data and trade execution toolkit.
- [Workbench](https://github.com/fremantle-industries/workbench) - `Elixir/Erlang` - From Idea to Execution - Manage your trading operation across a globally distributed cluster.
- [Prop](https://github.com/fremantle-industries/prop) - `Elixir/Erlang` - An open and opinionated trading platform using productive & familiar open source libraries and tools for strategy research, execution and operation.
- [Kelp](https://github.com/stellar/kelp) - `Golang` - Kelp is an open-source Golang algorithmic cryptocurrency trading bot that runs on centralized exchanges and Stellar DEX (command-line usage and desktop GUI).
- [TradeFrame](https://github.com/rburkholder/trade-frame) - `CPP` - C++ 17 based framework/library (with sample applications) for testing options based automated trading ideas using DTN IQ real time data feed and Interactive Brokers (TWS API) for trade execution. Comes with built-in [Option Greeks/IV](https://github.com/rburkholder/trade-frame/tree/master/lib/TFOptions) calculation library.
- [Hikyuu](https://github.com/fasiondog/hikyuu) - `Python` `C++` - A base on Python/C++ open source high-performance quant framework for faster analysis and backtesting, contains the complete trading system components for reuse and combination. You can use python or c++ freely.
- [OrderMatchingEngine](https://github.com/PIYUSH-KUMAR1809/order-matching-engine) - `CPP` - A production-grade, lock-free, high-frequency trading matching engine achieving 150M+ orders/sec.
- [PandoraTrader](https://github.com/pegasusTrader/PandoraTrader) - `CPP` - A C++ CTP trading framework, with very clear logic.
- [NexusFix](https://github.com/SilverstreamsAI/NexusFix) - `CPP` - C++23 FIX protocol engine with zero-copy parsing and SIMD acceleration, 3x faster than QuickFIX.
- [QuantConnect](https://github.com/QuantConnect/Lean) - `CSharp` - Lean Engine is an open-source fully managed C# algorithmic trading engine built for desktop and cloud usage.
- [StockSharp](https://github.com/StockSharp/StockSharp) - `CSharp` - Algorithmic trading and quantitative trading open source platform to develop trading robots (stock markets, forex, crypto, bitcoins, and options).
- [TDAmeritrade.DotNetCore](https://github.com/NVentimiglia/TDAmeritrade.DotNetCore) - `CSharp` - Free, open-source .NET Client for the TD Ameritrade Trading Platform. Helps developers integrate TD Ameritrade API into custom trading solutions.
- [Barter](https://github.com/barter-rs/barter-rs) - `Rust` - Open-source Rust framework for building event-driven live-trading & backtesting systems.
- [LFEST](https://github.com/MathisWellmann/lfest-rs) - `Rust` - Simulated perpetual futures exchange to trade your strategy against.
- [OpenFinClaw](https://github.com/cryptoSUN2049/openFinclaw) - `Python` `Rust` - AI-native one-person hedge fund platform with Rust trading engine. Natural language → strategy → backtest → execution in 60s. Multi-market (US/HK/CN/Crypto), self-evolving strategy pipeline. Built on OpenClaw (68K+ stars).

- [TradeClaw](https://github.com/naimkatiman/tradeclaw) - `Node.js` `TypeScript` - Open-source self-hosted AI trading signal platform. Generates buy/sell signals using RSI, MACD, EMA, Bollinger Bands for forex, crypto and commodities. Deployable via Docker Compose. ([Demo](https://tradeclaw.win/dashboard))
## Portfolio Optimization & Risk Analysis

- [skfolio](https://github.com/skfolio/skfolio) - `Python` - Python library for portfolio optimization built on top of scikit-learn. It provides a unified interface and sklearn compatible tools to build, tune and cross-validate portfolio models.
- [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) - `Python` - Financial portfolio optimization in python, including classical efficient frontier and advanced methods.
- [Eiten](https://github.com/tradytics/eiten) - `Python` - Eiten is an open source toolkit by Tradytics that implements various statistical and algorithmic investing strategies such as Eigen Portfolios, Minimum Variance Portfolios, Maximum Sharpe Ratio Portfolios, and Genetic Algorithms based Portfolios.
- [riskparity.py](https://github.com/dppalomar/riskparity.py) - `Python` - fast and scalable design of risk parity portfolios with TensorFlow 2.0.
- [mlfinlab](https://github.com/hudson-and-thames/mlfinlab) - `Python` - Implementations regarding "Advances in Financial Machine Learning" by Marcos Lopez de Prado. (Feature Engineering, Financial Data Structures, Meta-Labeling).
- [DeepDow](https://github.com/jankrepl/deepdow) - `Python` - Portfolio optimization with deep learning.
- [QuantLibRisks](https://github.com/auto-differentiation/QuantLib-Risks-Py) - `Python` - Fast risks with QuantLib.
- [XAD](https://github.com/auto-differentiation/xad-py) - `Python` - Automatic Differentation (AAD) Library.
- [pyfolio](https://github.com/quantopian/pyfolio) - `Python` - Portfolio and risk analytics in Python.
- [empyrical](https://github.com/quantopian/empyrical) - `Python` - Common financial risk and performance metrics.
- [fecon235](https://github.com/rsvp/fecon235) - `Python` - Computational tools for financial economics include: Gaussian Mixture model of leptokurtotic risk, adaptive Boltzmann portfolios.
- [finance](https://pypi.org/project/finance/) - `Python` - Financial Risk Calculations. Optimized for ease of use through class construction and operator overload.
- [qfrm](https://pypi.org/project/qfrm/) - `Python` - Quantitative Financial Risk Management: awesome OOP tools for measuring, managing and visualizing risk of financial instruments and portfolios. (Last updated: 2015-12-12).
- [visualize-wealth](https://github.com/benjaminmgross/visualize-wealth) - `Python` - Portfolio construction and quantitative analysis.
- [VisualPortfolio](https://github.com/wegamekinglc/VisualPortfolio) - `Python` - This tool is used to visualize the performance of a portfolio.
- [universal-portfolios](https://github.com/Marigold/universal-portfolios) - `Python` - Collection of algorithms for online portfolio selection.
- [FinQuant](https://github.com/fmilthaler/FinQuant) - `Python` - A program for financial portfolio management, analysis and optimization.
- [Empyrial](https://github.com/ssantoshp/Empyrial) - `Python` - Portfolio's risk and performance analytics and returns predictions.
- [risktools](https://github.com/bbcho/risktools-dev) - `Python` - Risk tools for use within the crude and crude products trading space with partial implementation of R's PerformanceAnalytics.
- [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib) - `Python` - Portfolio Optimization and Quantitative Strategic Asset Allocation in Python.
- [empyrical-reloaded](https://github.com/stefan-jansen/empyrical-reloaded) - `Python` - Common financial risk and performance metrics. [empyrical](https://github.com/quantopian/empyrical) fork.
- [pyfolio-reloaded](https://github.com/stefan-jansen/pyfolio-reloaded) - `Python` - Portfolio and risk analytics in Python. [pyfolio](https://github.com/quantopian/pyfolio) fork.
- [fortitudo.tech](https://github.com/fortitudo-tech/fortitudo.tech) - `Python` - Conditional Value-at-Risk (CVaR) portfolio optimization and Entropy Pooling views / stress-testing in Python.
- [quantitative-finance-tools](https://github.com/omichauhan-lgtm/quantitative-finance-tools) - `Python` - Library for portfolio optimization (MVO) and rigorous risk metrics (VaR/CVaR).
- [curistat](https://github.com/moxiespirit/MyClone/tree/main/volatility_platform) - `Python` - Futures volatility forecasting platform for ES/NQ. Proprietary CVN rating (1-10), regime detection (CRC composite), 8 directional signals, economic event impact analytics. Includes MCP server for AI agent integration.
- [Prop Trader Compass](https://otto-ships.github.io/prop-trader-compass/) - `Python` - Interactive risk and payout calculator for Futures and CFD traders; features one-time fee firm comparisons.
- [portfolio](https://github.com/dgerlanc/portfolio) - `R` - Analysing equity portfolios.
- [sparseIndexTracking](https://github.com/dppalomar/sparseIndexTracking) - `R` - Portfolio design to track an index.
- [riskParityPortfolio](https://github.com/dppalomar/riskParityPortfolio) - `R` - Blazingly fast design of risk parity portfolios.
- [PortfolioAnalytics](https://github.com/braverock/PortfolioAnalytics) - `R` - Portfolio Analysis, Including Numerical Methods for Optimizationof Portfolios.
- [PerformanceAnalytics](https://github.com/braverock/PerformanceAnalytics) - `R` - Econometric tools for performance and risk analysis.
- [OnlinePortfolioAnalytics.jl](https://github.com/femtotrader/OnlinePortfolioAnalytics.jl) - `Julia` - A Julia quantitative portfolio analytics (risk / performance) via online algorithms.
- [RiskPerf.jl](https://github.com/rbeeli/RiskPerf.jl) - `Julia` - Quantitative risk and performance analysis package for financial time series powered by the Julia language.
- [portfolio-allocation](https://github.com/lequant40/portfolio_allocation_js) - `JavaScript` - PortfolioAllocation is a JavaScript library designed to help constructing financial portfolios made of several assets: bonds, commodities, cryptocurrencies, currencies, exchange traded funds (ETFs), mutual funds, stocks...
- [Ghostfolio](https://github.com/ghostfolio/ghostfolio) - `JavaScript` - Wealth management software to keep track of financial assets like stocks, ETFs or cryptocurrencies and make solid, data-driven investment decisions.
- [rebalance](https://github.com/cjroth/rebalance) - `JavaScript` - Interactive portfolio rebalancing tool that imports brokerage CSV data, sets target allocations, and generates trade instructions.

## Factor Analysis

- [alphalens](https://github.com/quantopian/alphalens) - `Python` - Performance analysis of predictive alpha factors.
- [alphalens-reloaded](https://github.com/stefan-jansen/alphalens-reloaded) - `Python` - Performance analysis of predictive (alpha) stock factors.
- [Spectre](https://github.com/Heerozh/spectre) - `Python` - GPU-accelerated Factors analysis library and Backtester.
- [quant-lab-alpha](https://github.com/husainm97/quant-lab-alpha) - `Python` - Open-source investment analytics platform bridging academic research and retail finance.
- [covFactorModel](https://github.com/dppalomar/covFactorModel) - `R` - Covariance matrix estimation via factor models.
- [FactorAnalytics](https://github.com/braverock/FactorAnalytics) - `R` - The FactorAnalytics package contains fitting and analysis methods for the three main types of factor models used in conjunction with portfolio construction, optimization and risk management, namely fundamental factor models, time series factor models and statistical factor models.
- [Expected Returns](https://github.com/JustinMShea/ExpectedReturns) - `R` - Solutions for enhancing portfolio diversification and replications of seminal papers with R, most of which are discussed in one of the best investment references of the recent decade, Expected Returns: An Investors Guide to Harvesting Market Rewards by Antti Ilmanen.

## Sentiment Analysis & Alternative Data

- [Asset News Sentiment Analyzer](https://github.com/KVignesh122/AssetNewsSentimentAnalyzer) - `Python` - Sentiment analysis and report generation package for financial assets and securities utilizing GPT models.
- [Social Stock Sentiment API](https://api.adanos.org/docs) - `Python` - REST API analyzing Reddit and X/Twitter for stock mentions and sentiment, providing buzz scores, trending stocks, and AI-generated trend explanations.

## Time Series Analysis

- [ARCH](https://github.com/bashtage/arch) - `Python` - ARCH models in Python.
- [statsmodels](http://statsmodels.sourceforge.net) - `Python` - Python module that allows users to explore data, estimate statistical models, and perform statistical tests. [GitHub](https://github.com/statsmodels/statsmodels)
- [dynts](https://github.com/quantmind/dynts) - `Python` - Python package for timeseries analysis and manipulation.
- [PyFlux](https://github.com/RJT1990/pyflux) - `Python` - Python library for timeseries modelling and inference (frequentist and Bayesian) on models.
- [tsfresh](https://github.com/blue-yonder/tsfresh) - `Python` - Automatic extraction of relevant features from time series.
- [Facebook Prophet](https://github.com/facebook/prophet) - `Python` - Tool for producing high quality forecasts for time series data that has multiple seasonality with linear or non-linear growth.
- [tsmoothie](https://github.com/cerlymarco/tsmoothie) - `Python` - A python library for time-series smoothing and outlier detection in a vectorized way.
- [pmdarima](https://github.com/alkaline-ml/pmdarima) - `Python` - A statistical library designed to fill the void in Python's time series analysis capabilities, including the equivalent of R's auto.arima function.
- [gluon-ts](https://github.com/awslabs/gluon-ts) - `Python` - vProbabilistic time series modeling in Python.
- [OmniOracle](https://github.com/cesabici-bit/omni-oracle) - `Python` - Automatic discovery of non-trivial statistical relationships across 500+ time series from FRED, World Bank, EIA, and NOAA using mutual information screening, lagged MI directional testing, and FDR correction.
- [functime](https://github.com/functime-org/functime) - `Python` - Time-series machine learning at scale. Built with Polars for embarrassingly parallel feature extraction and forecasts on panel data.
- [tseries](https://cran.r-project.org/web/packages/tseries/index.html) - `R` - Time Series Analysis and Computational Finance.
- [fGarch](https://cran.r-project.org/web/packages/fGarch/index.html) - `R` - Rmetrics - Autoregressive Conditional Heteroskedastic Modelling.
- [timeSeries](https://cran.r-project.org/web/packages/timeSeries/index.html) - `R` - Rmetrics - Financial Time Series Objects.
- [rugarch](https://github.com/alexiosg/rugarch) - `R` - Univariate GARCH Models.
- [rmgarch](https://github.com/alexiosg/rmgarch) - `R` - Multivariate GARCH Models.
- [tidypredict](https://github.com/edgararuiz/tidypredict) - `R` - Run predictions inside the database <https://tidypredict.netlify.com/>.
- [tidyquant](https://github.com/business-science/tidyquant) - `R` - Bringing financial analysis to the tidyverse.
- [timetk](https://github.com/business-science/timetk) - `R` - A toolkit for working with time series in R.
- [tibbletime](https://github.com/business-science/tibbletime) - `R` - Built on top of the tidyverse, tibbletime is an extension that allows for the creation of time aware tibbles through the setting of a time index.
- [matrixprofile](https://github.com/matrix-profile-foundation/matrixprofile) - `R` - Time series data mining library built on top of the novel Matrix Profile data structure and algorithms.
- [garchmodels](https://github.com/AlbertoAlmuinha/garchmodels) - `R` - A parsnip backend for GARCH models.
- [TimeSeries.jl](https://github.com/JuliaStats/TimeSeries.jl) - `Julia` - Time series toolkit for Julia.
- [TimeFrames.jl](https://github.com/femtotrader/TimeFrames.jl) - `Julia` - A Julia library that defines TimeFrame (essentially for resampling TimeSeries).

## Market Data & Data Sources

- [OpenBB Terminal](https://github.com/OpenBB-finance/OpenBBTerminal) - `Python` - Terminal for investment research for everyone.
- [Fincept Terminal](https://github.com/Fincept-Corporation/FinceptTerminal) - `Python` - Advance Data Based A.I Terminal for all Types of Financial Asset Research.
- [yfinance](https://github.com/ranaroussi/yfinance) - `Python` - Yahoo! Finance market data downloader (+faster Pandas Datareader).
- [defeatbeta-api](https://github.com/defeat-beta/defeatbeta-api) - `Python` - An open-source alternative to Yahoo Finance's market data APIs with higher reliability.
- [findatapy](https://github.com/cuemacro/findatapy) - `Python` - Python library to download market data via Bloomberg, Quandl, Yahoo etc.
- [googlefinance](https://github.com/hongtaocai/googlefinance) - `Python` - Python module to get real-time stock data from Google Finance API.
- [yahoo-finance](https://github.com/lukaszbanasiak/yahoo-finance) - `Python` - Python module to get stock data from Yahoo! Finance.
- [pandas-datareader](https://github.com/pydata/pandas-datareader) - `Python` - Python module to get data from various sources (Google Finance, Yahoo Finance, FRED, OECD, Fama/French, World Bank, Eurostat...) into Pandas datastructures such as DataFrame, Panel with a caching mechanism.
- [pandas-finance](https://github.com/davidastephens/pandas-finance) - `Python` - High level API for access to and analysis of financial data.
- [pyhoofinance](https://github.com/innes213/pyhoofinance) - `Python` - Rapidly queries Yahoo Finance for multiple tickers and returns typed data for analysis.
- [yfinanceapi](https://github.com/Karthik005/yfinanceapi) - `Python` - Finance API for Python.
- [yql-finance](https://github.com/slawek87/yql-finance) - `Python` - yql-finance is simple and fast. API returns stock closing prices for current period of time and current stock ticker (i.e. APPL, GOOGL).
- [ystockquote](https://github.com/cgoldberg/ystockquote) - `Python` - Retrieve stock quote data from Yahoo Finance.
- [jugaad-data](https://github.com/jugaad-py/jugaad-data) - `Python` - Download historical and live stock data from NSE (National Stock Exchange of India), BSE, and RBI.
- [nsetools](https://github.com/vsjha18/nsetools) - `Python` - Python library for extracting real-time data from National Stock Exchange (India).
- [bsedata](https://github.com/sdrdis/bsedata) - `Python` - Python library for extracting real-time data from Bombay Stock Exchange (India).
- [nse-insights-api](https://github.com/pratik-choudhari/nse-insights) - `Python` - Unofficial NSE India API for stock quotes, indices, historical data and more.
- [wallstreet](https://github.com/mcdallas/wallstreet) - `Python` - Real time stock and option data.
- [stock_extractor](https://github.com/ZachLiuGIS/stock_extractor) - `Python` - General Purpose Stock Extractors from Online Resources.
- [Stockex](https://github.com/cttn/Stockex) - `Python` - Python wrapper for Yahoo! Finance API.
- [SwapAPI](https://swapapi.dev) - `Python` - Free DEX aggregator API returning executable swap calldata across 46 EVM chains. No API key required. [GitHub](https://github.com/swap-api/swap-api)
- [finsymbols](https://github.com/skillachie/finsymbols) - `Python` - Obtains stock symbols and relating information for SP500, AMEX, NYSE, and NASDAQ.
- [FRB](https://github.com/avelkoski/FRB) - `Python` - Python Client for FRED® API.
- [inquisitor](https://github.com/econdb/inquisitor) - `Python` - Python Interface to Econdb.com API.
- [yfi](https://github.com/nickelkr/yfi) - `Python` - Yahoo! YQL library.
- [chinesestockapi](https://pypi.org/project/chinesestockapi/) - `Python` - Python API to get Chinese stock price. (Last updated: 2015-03-21).
- [exchange](https://github.com/akarat/exchange) - `Python` - Get current exchange rate.
- [ticks](https://github.com/jamescnowell/ticks) - `Python` - Simple command line tool to get stock ticker data.
- [pybbg](https://github.com/bpsmith/pybbg) - `Python` - Python interface to Bloomberg COM APIs.
- [ccy](https://github.com/lsbardel/ccy) - `Python` - Python module for currencies.
- [tushare](https://pypi.org/project/tushare/) - `Python` - A utility for crawling historical and Real-time Quotes data of China stocks. (Last updated: 2024-08-27).
- [edinetdb](https://edinetdb.com/) - `Python` - Free API and MCP server for Japanese company financials. Normalizes EDINET XBRL across JP-GAAP, IFRS, and US-GAAP for 3,800+ listed companies with 90 metrics, screening, and securities report text.
- [edinet-mcp](https://github.com/ajtgjmdjp/edinet-mcp) - `Python` - Parse Japanese XBRL financial statements from EDINET with 161 normalized labels, 26 financial metrics, and multi-company screening.
- [estat-mcp](https://github.com/ajtgjmdjp/estat-mcp) - `Python` - Access Japanese government statistics (e-Stat) covering population, GDP, CPI, labor, and trade data with MCP integration and Polars export.
- [tdnet-disclosure-mcp](https://github.com/ajtgjmdjp/tdnet-disclosure-mcp) - `Python` - Access Japanese timely disclosures (TDNet) via MCP. Retrieve earnings, dividends, forecasts, buybacks, and other filings for 4,000+ listed companies. No API key required.
- [cn_stock_src](https://github.com/jealous/cn_stock_src) - `Python` - Utility for retrieving basic China stock data from different sources.
- [coinmarketcap](https://github.com/barnumbirr/coinmarketcap) - `Python` - Python API for coinmarketcap.
- [coinpulse](https://github.com/soutone/coinpulse-python) - `Python` - Python SDK for cryptocurrency portfolio tracking with real-time prices, P/L calculations, and price alerts. Free tier available.
- [after-hours](https://github.com/datawrestler/after-hours) - `Python` - Obtain pre market and after hours stock prices for a given symbol.
- [bronto-python](https://pypi.org/project/bronto-python/) - `Python` - Bronto API Integration for Python. [GitHub](https://github.com/Scotts-Marketplace/bronto-python)
- [pytdx](https://github.com/rainx/pytdx) - `Python` - Python Interface for retrieving chinese stock realtime quote data from TongDaXin Nodes.
- [pdblp](https://github.com/matthewgilbert/pdblp) - `Python` - A simple interface to integrate pandas and the Bloomberg Open API.
- [tiingo](https://github.com/hydrosquall/tiingo-python) - `Python` - Python interface for daily composite prices/OHLC/Volume + Real-time News Feeds, powered by the Tiingo Data Platform.
- [iexfinance](https://github.com/addisonlynch/iexfinance) - `Python` - Python Interface for retrieving real-time and historical prices and equities data from The Investor's Exchange.
- [pyEX](https://github.com/timkpaine/pyEX) - `Python` - Python interface to IEX with emphasis on pandas, support for streaming data, premium data, points data (economic, rates, commodities), and technical indicators.
- [alpaca-trade-api](https://github.com/alpacahq/alpaca-trade-api-python) - `Python` - Python interface for retrieving real-time and historical prices from Alpaca API as well as trade execution.
- [metatrader5](https://pypi.org/project/MetaTrader5/) - `Python` - API Connector to MetaTrader 5 Terminal. (Last updated: 2026-02-20).
- [akshare](https://github.com/jindaxiang/akshare) - `Python` - AkShare is an elegant and simple financial data interface library for Python, built for human beings! <https://akshare.readthedocs.io>.
- [yahooquery](https://github.com/dpguthrie/yahooquery) - `Python` - Python interface for retrieving data through unofficial Yahoo Finance API.
- [investpy](https://github.com/alvarobartt/investpy) - `Python` - Financial Data Extraction from Investing.com with Python! <https://investpy.readthedocs.io/>.
- [yliveticker](https://github.com/yahoofinancelive/yliveticker) - `Python` - Live stream of market data from Yahoo Finance websocket.
- [bbgbridge](https://github.com/ran404/bbgbridge) - `Python` - Easy to use Bloomberg Desktop API wrapper for Python.
- [polygon.io](https://github.com/polygon-io/client-python) - `Python` - A python library for Polygon.io financial data APIs.
- [alpha_vantage](https://github.com/RomelTorres/alpha_vantage) - `Python` - A python wrapper for Alpha Vantage API for financial data.
- [oilpriceapi](https://github.com/OilpriceAPI/python-sdk) - `Python` - Python SDK for real-time oil and commodity prices (WTI, Brent, Urals, natural gas, coal) with OpenBB integration.
- [FinanceDataReader](https://github.com/FinanceData/FinanceDataReader) - `Python` - Open Source Financial data reader for U.S, Korean, Japanese, Chinese, Vietnamese Stocks.
- [pystlouisfed](https://github.com/TomasKoutek/pystlouisfed) - `Python` - Python client for Federal Reserve Bank of St. Louis API - FRED, ALFRED, GeoFRED and FRASER.
- [python-bcb](https://github.com/wilsonfreitas/python-bcb) - `Python` - Python interface to Brazilian Central Bank web services.
- [swiss-finance-data](https://github.com/EMen11/swiss-finance-data) - `Python` - Python package for Swiss financial data (SNB Policy Rate, SARON, CHF FX rates, CPI, SMI equities, Confederation bond yields) from official SNB sources.
- [market-prices](https://github.com/maread99/market_prices) - `Python` - Create meaningful OHLCV datasets from knowledge of [exchange-calendars](https://github.com/gerrymanoim/exchange_calendars) (works out-the-box with data from Yahoo Finance).
- [tardis-python](https://github.com/tardis-dev/tardis-python) - `Python` - Python interface for Tardis.dev high frequency crypto market data.
- [lake-api](https://github.com/crypto-lake/lake-api) - `Python` - Python interface for Crypto Lake high frequency crypto market data.
- [tessa](https://github.com/ymyke/tessa) - `Python` - simple, hassle-free access to price information of financial assets (currently based on yfinance and pycoingecko), including search and a symbol class.
- [pandaSDMX](https://github.com/dr-leo/pandaSDMX) - `Python` - Python package that implements SDMX 2.1 (ISO 17369:2013), a format for exchange of statistical data and metadata used by national statistical agencies, central banks, and international organisations.
- [cif](https://github.com/LenkaV/CIF) - `Python` - Python package that include few composite indicators, which summarize multidimensional relationships between individual economic indicators.
- [finagg](https://github.com/theOGognf/finagg) - `Python` - finagg is a Python package that provides implementations of popular and free financial APIs, tools for aggregating historical data from those APIs into SQL databases, and tools for transforming aggregated data into features useful for analysis and AI/ML.
- [FinanceDatabase](https://github.com/JerBouma/FinanceDatabase) - `Python` - This is a database of 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets.
- [Trading Strategy](https://github.com/tradingstrategy-ai/trading-strategy/) - `Python` - download price data for decentralised exchanges and lending protocols (DeFi).
- [datamule-python](https://github.com/john-friedman/datamule-python) - `Python` - A package to work with SEC data. Incorporates datamule endpoints.
- [fsynth](https://github.com/welcra/fsynth) - `Python` - Python library for high-fidelity unlimited synthetic financial data generation using Heston Stochastic Volatility and Merton Jump Diffusion.
- [fedfred](https://nikhilxsunder.github.io/fedfred/) - `Python` - FRED & GeoFRED Economic data API with preprocessed dataframe output in pandas/geopandas, polars/polars_st, and dask dataframes/geodataframes.
- [edgar-sec](https://nikhilxsunder.github.io/edgar-sec/) - `Python` - EDGAR Financial data API with preprocessed dataclass outputs.
- [edgartools](https://github.com/dgunning/edgartools) - `Python` - AI-native SEC EDGAR library with XBRL financials, clean text extraction, 17+ typed forms, and pandas DataFrames.
- [FXMacroData](https://fxmacrodata.com/) - `Python` - Real-time forex macroeconomic API for all major currency pairs sourced from central bank announcements. [GitHub](https://github.com/fxmacrodata/fxmacrodata)
- [uk-sic-codes](https://github.com/borschai/uk-sic-codes) - `Python` - UK SIC 2007 industry classification code lookup, search, and validation. 731 codes, 21 sections. [PyPI](https://pypi.org/project/uk-sic-codes/)
- [uk-company-number](https://github.com/borschai/uk-company-number) - `Python` - Validate, format, and identify UK Companies House company numbers. Supports all 27 prefixes. [PyPI](https://pypi.org/project/uk-company-number/)
- [IBrokers](https://cran.r-project.org/web/packages/IBrokers/index.html) - `R` - Provides native R access to Interactive Brokers Trader Workstation API.
- [Rblpapi](https://github.com/Rblp/Rblpapi) - `R` - An R Interface to 'Bloomberg' is provided via the 'Blp API'.
- [Rbitcoin](https://github.com/jangorecki/Rbitcoin) - `R` - Unified markets API interface (bitstamp, kraken, btce, bitmarket).
- [GetTDData](https://github.com/msperlin/GetTDData) - `R` - Downloads and aggregates data for Brazilian government issued bonds directly from the website of Tesouro Direto.
- [GetHFData](https://github.com/msperlin/GetHFData) - `R` - Downloads and aggregates high frequency trading data for Brazilian instruments directly from Bovespa ftp site.
- [td](https://github.com/eddelbuettel/td) - `R` - Interfaces the 'twelvedata' API for stocks and (digital and standard) currencies.
- [rbcb](https://github.com/wilsonfreitas/rbcb) - `R` - R interface to Brazilian Central Bank web services.
- [rb3](https://github.com/ropensci/rb3) - `R` - A bunch of downloaders and parsers for data delivered from B3.
- [simfinapi](https://github.com/matthiasgomolka/simfinapi) - `R` - Makes 'SimFin' data (<https://simfin.com/>) easily accessible in R.
- [tidyfinance](https://github.com/tidy-finance/r-tidyfinance) - `R` - Tidy Finance helper functions to download financial data and process the raw data into a structured Format (tidy data), including.
- [CcyConv.jl](https://github.com/bhftbootcamp/CcyConv.jl) - `Julia` - Currency conversion library for Julia.
- [CryptoExchangeAPIs.jl](https://github.com/bhftbootcamp/CryptoExchangeAPIs.jl) - `Julia` - A Julia library for cryptocurrency exchange APIs.
- [MarketData.jl](https://github.com/JuliaQuant/MarketData.jl) - `Julia` - Time series market data.
- [OnlineResamplers.jl](https://github.com/femtotrader/OnlineResamplers.jl) - `Julia` - High-performance Julia package for real-time resampling of financial market data.
- [PENDAX](https://github.com/CompendiumFi/PENDAX-SDK) - `JavaScript` - Javascript SDK for Trading/Data API and Websockets for FTX, FTXUS, OKX, Bybit, & More.
- [PreReason](https://github.com/PreReason/mcp) - `JavaScript` - Pre-analyzed Bitcoin and macro market briefings for AI agents. 17 contexts with trend signals, confidence scores, and regime classification via REST API and MCP.
- [marketstore](https://github.com/alpacahq/marketstore) - `Golang` - DataFrame Server for Financial Timeseries Data.
- [fin-stream](https://github.com/Mattbusel/fin-stream) - `Rust` - Real-time market data streaming in Rust: lock-free SPSC ring buffer, 100K+ ticks/second ingestion, multi-timeframe OHLCV construction, and Lorentz transforms on financial time series.
- [finalytics](https://github.com/Nnamdi-sys/finalytics) - `Rust` - A rust library for financial data analysis.

## Prediction Markets

- [pmxt](https://github.com/pmxt-dev/pmxt) - `Python` `JavaScript` - The CCXT for prediction markets. A unified API for trading on Polymarket, Kalshi, and more.
- [polymarket-whales](https://github.com/al1enjesus/polymarket-whales) - `Python` - Real-time whale trade tracker for Polymarket — terminal alerts + Telegram notifications when large orders hit the book.
- [Polymarket Scanner API](https://github.com/vesper-astrena/polymarket-scanner-api) - `Python` - Real-time arbitrage detection API for Polymarket prediction markets, scanning 12,000+ markets for mispricings.
- [SimpleFunctions](https://github.com/spfunctions/simplefunctions-cli) - `JavaScript` - Prediction market intelligence CLI for Kalshi and Polymarket. Causal thesis models, edge detection, 24/7 orderbook monitoring, what-if scenarios, and trade execution. MCP server for AI agent integration.
- [pmxt](https://github.com/pmxt-dev/pmxt) - `Python` `JavaScript` - The CCXT for prediction markets. A unified API for trading on Polymarket, Kalshi, and more.

## Calendars & Market Hours

- [exchange_calendars](https://github.com/gerrymanoim/exchange_calendars) - `Python` - Stock Exchange Trading Calendars.
- [bizdays](https://github.com/wilsonfreitas/python-bizdays) - `Python` - Business days calculations and utilities.
- [pandas_market_calendars](https://github.com/rsheftel/pandas_market_calendars) - `Python` - Exchange calendars to use with pandas for trading applications.
- [timeDate](https://cran.r-project.org/web/packages/timeDate/index.html) - `R` - Chronological and Calendar Objects.
- [bizdays](https://github.com/wilsonfreitas/R-bizdays) - `R` - Business days calculations and utilities.

## Visualization

- [D-Tale](https://github.com/man-group/dtale) - `Python` - Visualizer for pandas dataframes and xarray datasets.
- [mplfinance](https://github.com/matplotlib/mplfinance) - `Python` - matplotlib utilities for the visualization, and visual analysis, of financial data.
- [finplot](https://github.com/highfestiva/finplot) - `Python` - Performant and effortless finance plotting for Python.
- [finvizfinance](https://github.com/lit26/finvizfinance) - `Python` - Finviz analysis python library.
- [market-analy](https://github.com/maread99/market_analy) - `Python` - Analysis and interactive charting using [market-prices](https://github.com/maread99/market_prices) and bqplot.
- [QuantInvestStrats](https://github.com/ArturSepp/QuantInvestStrats) - `Python` - Quantitative Investment Strategies (QIS) package implements Python analytics for visualisation of financial data, performance reporting, analysis of quantitative strategies.
- [LightweightCharts.jl](https://github.com/bhftbootcamp/LightweightCharts.jl) - `Julia` - Julia wrapper for Lightweight Charts™ by TradingView.
- [QUANTAXIS_Webkit](https://github.com/yutiansut/QUANTAXIS_Webkit) - `JavaScript` - An awesome visualization center based on quantaxis.

## Excel & Spreadsheet Integration

- [xlwings](https://www.xlwings.org/) - `Python` - Make Excel fly with Python. [GitHub](https://github.com/xlwings/xlwings)
- [openpyxl](https://openpyxl.readthedocs.io/en/latest/) - `Python` - Read/Write Excel 2007 xlsx/xlsm files.
- [xlrd](https://github.com/python-excel/xlrd) - `Python` - Library for developers to extract data from Microsoft Excel spreadsheet files.
- [xlsxwriter](https://xlsxwriter.readthedocs.io/) - `Python` - Write files in the Excel 2007+ XLSX file format. [GitHub](https://github.com/jmcnamara/XlsxWriter)
- [xlwt](https://github.com/python-excel/xlwt) - `Python` - Library to create spreadsheet files compatible with MS Excel 97/2000/XP/2003 XLS files, on any platform.
- [xlloop](http://xlloop.sourceforge.net) - `Python` - XLLoop is an open source framework for implementing Excel user-defined functions (UDFs) on a centralised server (a function server). [GitHub](https://github.com/poidasmith/xlloop)
- [expy](http://www.bnikolic.co.uk/expy/expy.html) - `Python` - The ExPy add-in allows easy use of Python directly from within an Microsoft Excel spreadsheet, both to execute arbitrary code and to define new Excel functions.
- [pyxll](https://www.pyxll.com) - `Python` - PyXLL is an Excel add-in that enables you to extend Excel using nothing but Python code.

## Quant Research Environments

- [Jupyter Quant](https://github.com/gnzsnz/jupyter-quant) - `Python` - A dockerized Jupyter quant research environment with preloaded tools for quant analysis, statsmodels, pymc, arch, py_vollib, zipline-reloaded, PyPortfolioOpt, etc.

## Cross-Language Frameworks

- [RunMat](https://runmat.org) - High performance, Open Source, MATLAB syntax runtime. [GitHub](https://github.com/runmat-org/runmat)
- [QuantLib](https://github.com/lballabio/QuantLib) - The QuantLib project is aimed at providing a comprehensive software framework for quantitative finance.
- [QuantLibRisks](https://github.com/auto-differentiation/QuantLib-Risks-Cpp) - Fast risks with QuantLib in C++.
- [XAD](https://github.com/auto-differentiation/xad) - Automatic Differentation (AAD) Library.
- [QuantLib](https://github.com/lballabio/QuantLib) - The QuantLib project is aimed at providing a comprehensive software framework for quantitative finance.
  - QuantLibRisks - Fast risks with QuantLib in [Python](https://pypi.org/project/QuantLib-Risks/) and [C++](https://github.com/auto-differentiation/QuantLib-Risks-Cpp)
  - XAD - Automatic Differentiation (AAD) Library in [Python](https://pypi.org/project/xad/) and [C++](https://github.com/auto-differentiation/xad/)
  - [JQuantLib](https://github.com/frgomes/jquantlib) - Java port.
  - [RQuantLib](https://github.com/eddelbuettel/rquantlib) - R port.
  - [QuantLibAddin](https://www.quantlib.org/quantlibaddin/) - Excel support.
  - [QuantLibXL](https://www.quantlib.org/quantlibxl/) - Excel support.
  - [QLNet](https://github.com/amaggiulli/qlnet) - .Net port.
  - [PyQL](https://github.com/enthought/pyql) - Python port.
  - [QuantLib.jl](https://github.com/pazzo83/QuantLib.jl) - Julia port.
  - [QuantLib-Python Documentation](https://quantlib-python-docs.readthedocs.io/) - Documentation for the Python bindings for the QuantLib library.
- [TA-Lib](https://ta-lib.org) - perform technical analysis of financial market data. [GitHub](https://github.com/TA-Lib/ta-lib)
  - [ta-lib-python](https://github.com/TA-Lib/ta-lib-python)
  - [ta-lib](https://github.com/TA-Lib/ta-lib)
- [RunMat](https://github.com/runmat-org/runmat) - Rust runtime for MATLAB-syntax array math with automatic CPU/GPU execution and fused kernels for quant simulations.

## Reproducing Works, Training & Books

- [Special-Relativity-in-Financial-Modeling](https://github.com/Mattbusel/Special-Relativity-in-Financial-Modeling) - C++20 implementation of special-relativistic geometry applied to OHLCV data: Lorentz factors, spacetime intervals, Christoffel symbols, and geodesic deviation signals from live market data. DOI: 10.5281/zenodo.18639919.
- [Auto-Differentiation Website](https://auto-differentiation.github.io/) - Background and  resources on Automatic Differentiation (AD) / Adjoint Algorithmic Differentitation (AAD).
- [Derman Papers](https://github.com/MarcosCarreira/DermanPapers) - Notebooks that replicate original quantitative finance papers from Emanuel Derman.
- [volatility-trading](https://github.com/jasonstrimpel/volatility-trading) - A complete set of volatility estimators based on Euan Sinclair's Volatility Trading.
- [quant](https://github.com/paulperry/quant) - Quantitative Finance and Algorithmic Trading exhaust; mostly ipython notebooks based on Quantopian, Zipline, or Pandas.
- [fecon235](https://github.com/rsvp/fecon235) - Open source project for software tools in financial economics. Many jupyter notebook to verify theoretical ideas and practical methods interactively.
- [Quantitative-Notebooks](https://github.com/LongOnly/Quantitative-Notebooks) - Educational notebooks on quantitative finance, algorithmic trading, financial modelling and investment strategy.
- [QuantEcon](https://quantecon.org/) - Lecture series on economics, finance, econometrics and data science; QuantEcon.py, QuantEcon.jl, notebooks.
- [FinanceHub](https://github.com/Finance-Hub/FinanceHub) - Resources for Quantitative Finance.
- [Python_Option_Pricing](https://github.com/dedwards25/Python_Option_Pricing) - An library to price financial options written in Python. Includes: Black Scholes, Black 76, Implied Volatility, American, European, Asian, Spread Options.
- [python-training](https://github.com/jpmorganchase/python-training) - J.P. Morgan's Python training for business analysts and traders.
- [Stock_Analysis_For_Quant](https://github.com/LastAncientOne/Stock_Analysis_For_Quant) - Different Types of Stock Analysis in Excel, Matlab, Power BI, Python, R, and Tableau.
- [algorithmic-trading-with-python](https://github.com/chrisconlan/algorithmic-trading-with-python) - Source code for Algorithmic Trading with Python (2020) by Chris Conlan.
- [MEDIUM_NoteBook](https://github.com/cerlymarco/MEDIUM_NoteBook) - Repository containing notebooks of [cerlymarco](https://github.com/cerlymarco)'s posts on Medium.
- [QuantFinance](https://github.com/PythonCharmers/QuantFinance) - Training materials in quantitative finance.
- [IPythonScripts](https://github.com/mgroncki/IPythonScripts) - Tutorials about Quantitative Finance in Python and QuantLib: Pricing, xVAs, Hedging, Portfolio Optimisation, Machine Learning and Deep Learning.
- [Computational-Finance-Course](https://github.com/LechGrzelak/Computational-Finance-Course) - Materials for the course of Computational Finance.
- [Machine-Learning-for-Asset-Managers](https://github.com/emoen/Machine-Learning-for-Asset-Managers) - Implementation of code snippets, exercises and application to live data from Machine Learning for Asset Managers (Elements in Quantitative Finance) written by Prof. Marcos López de Prado.
- [Python-for-Finance-Cookbook](https://github.com/PacktPublishing/Python-for-Finance-Cookbook) - Python for Finance Cookbook, published by Packt.
- [modelos_vol_derivativos](https://github.com/ysaporito/modelos_vol_derivativos) - "Modelos de Volatilidade para Derivativos" book's Jupyter notebooks.
- [NMOF](https://github.com/enricoschumann/NMOF) - Functions, examples and data from the first and the second edition of "Numerical Methods and Optimization in Finance" by M. Gilli, D. Maringer and E. Schumann (2019, ISBN:978-0128150658).
- [py4fi2nd](https://github.com/yhilpisch/py4fi2nd) - Jupyter Notebooks and code for Python for Finance (2nd ed., O'Reilly) by Yves Hilpisch.
- [aiif](https://github.com/yhilpisch/aiif) - Jupyter Notebooks and code for the book Artificial Intelligence in Finance (O'Reilly) by Yves Hilpisch.
- [py4at](https://github.com/yhilpisch/py4at) - Jupyter Notebooks and code for the book Python for Algorithmic Trading (O'Reilly) by Yves Hilpisch.
- [dawp](https://github.com/yhilpisch/dawp) - Jupyter Notebooks and code for Derivatives Analytics with Python (Wiley Finance) by Yves Hilpisch.
- [dx](https://github.com/yhilpisch/dx) - DX Analytics | Financial and Derivatives Analytics with Python.
- [QuantFinanceBook](https://github.com/LechGrzelak/QuantFinanceBook) - Quantitative Finance book.
- [rough_bergomi](https://github.com/ryanmccrickerd/rough_bergomi) - A Python implementation of the rough Bergomi model.
- [frh-fx](https://github.com/ryanmccrickerd/frh-fx) - A python implementation of the fast-reversion Heston model of Mechkov for FX purposes.
- [Value Investing Studies](https://github.com/euclidjda/value-investing-studies) - A collection of data analysis studies that examine the performance and characteristics of value investing over long periods of time.
- [Machine Learning Asset Management](https://github.com/firmai/machine-learning-asset-management) - Machine Learning in Asset Management (by @firmai).
- [Deep Learning Machine Learning Stock](https://github.com/LastAncientOne/Deep-Learning-Machine-Learning-Stock) - Deep Learning and Machine Learning stocks represent a promising long-term or short-term opportunity for investors and traders.
- [Technical Analysis and Feature Engineering](https://github.com/jo-cho/Technical_Analysis_and_Feature_Engineering) - Feature Engineering and Feature Importance of Machine Learning in Financial Market.
- [Differential Machine Learning and Axes that matter by Brian Huge and Antoine Savine](https://github.com/differential-machine-learning/notebooks) - Implement, demonstrate, reproduce and extend the results of the Risk articles 'Differential Machine Learning' (2020) and 'PCA with a Difference' (2021) by Huge and Savine, and cover implementation details left out from the papers.
- [systematictradingexamples](https://github.com/robcarver17/systematictradingexamples) - Examples of code related to book [Systematic Trading](www.systematictrading.org) and [blog](http://qoppac.blogspot.com).
- [pysystemtrade_examples](https://github.com/robcarver17/pysystemtrade_examples) - Examples using pysystemtrade for Robert Carver's [blog](http://qoppac.blogspot.com).
- [ML_Finance_Codes](https://github.com/mfrdixon/ML_Finance_Codes) - Machine Learning in Finance: From Theory to Practice Book.
- [Hands-On Machine Learning for Algorithmic Trading](https://github.com/packtpublishing/hands-on-machine-learning-for-algorithmic-trading) - Hands-On Machine Learning for Algorithmic Trading, published by Packt.
- [financialnoob-misc](https://github.com/financialnoob/misc) - Codes from @financialnoob's posts.
- [MesoSim Options Trading Strategy Library](https://github.com/deltaray-io/strategy-library) - Free and public Options Trading strategy library for MesoSim.
- [Quant-Finance-With-Python-Code](https://github.com/lingyixu/Quant-Finance-With-Python-Code) - Repo for code examples in Quantitative Finance with Python by Chris Kelliher.
- [QuantFinanceTraining](https://github.com/JoaoJungblut/QuantFinanceTraining) - This repository contains codes that were executed during my training in the CQF (Certificate in Quantitative Finance). The codes are organized by class, facilitating navigation and reference.
- [Statistical-Learning-based-Portfolio-Optimization](https://github.com/YannickKae/Statistical-Learning-based-Portfolio-Optimization) - This R Shiny App utilizes the Hierarchical Equal Risk Contribution (HERC) approach, a modern portfolio optimization method developed by Raffinot (2018).
- [book_irds3](https://github.com/attack68/book_irds3) - Code repository for Pricing and Trading Interest Rate Derivatives.
- [Autoencoder-Asset-Pricing-Models](https://github.com/RichardS0268/Autoencoder-Asset-Pricing-Models) - Reimplementation of Autoencoder Asset Pricing Models ([GKX, 2019](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3335536)).
- [Finance](https://github.com/shashankvemuri/Finance) - 150+ quantitative finance Python programs to help you gather, manipulate, and analyze stock market data.
- [101_formulaic_alphas](https://github.com/ram-ki/101_formulaic_alphas) - Implementation of [101 formulaic alphas](https://arxiv.org/ftp/arxiv/papers/1601/1601.00991.pdf) using qstrader.
- [Tidy Finance](https://www.tidy-finance.org/) - An opinionated approach to empirical research in financial economics - a fully transparent, open-source code base in multiple programming languages (Python and R) to enable the reproducible implementation of financial research projects for students and practitioners.
- [RoughVolatilityWorkshop](https://github.com/jgatheral/RoughVolatilityWorkshop) - 2024 QuantMind's Rough Volatility Workshop lectures.
- [AFML](https://github.com/boyboi86/AFML) - All the answers for exercises from Advances in Financial Machine Learning by Dr Marco Lopez de Parodo.
- [AlgoTradingLib](https://github.com/usdaud/algotradinglib.github.io) - A catalog of algorithmic trading libraries, frameworks, strategies, and educational materials.
- [Portfolio Optimization Book](https://portfoliooptimizationbook.com/) - Prof. Daniel Palomar's Portfolio Optimization Book. [GitHub](https://github.com/dppalomar/pob)

## Commercial & Proprietary Services

- [Chartscout](https://chartscout.io) - Real-time cryptocurrency chart pattern detection with automated alerts across multiple exchanges.
- [DayTradingBench](https://daytradingbench.com) - Live autonomous benchmark that evaluates LLM trading performance on DAX and Nasdaq indices using identical strategies and real-time market data. API access available.
- [CoinTester](https://cointester.io) - No-code crypto backtesting platform with 100+ indicators, AI sentiment signals, and 5+ years of historical data across 1,000+ trading pairs.
- [goMacro.ai](https://gomacro.ai) - AI-powered economic calendar with institutional-grade insights, bull/bear/base case scenario planning for NFP, CPI, PPI and other macro data releases.
- [StockAInsights](https://stockainsights.com) - AI-extracted financial statements API covering SEC filings including foreign filers (20-F, 6-K, 40-F), normalized quarterly and annual data from 2014+.
- [brapi.dev](https://brapi.dev/) - Brazilian stock market data API for B3/Bovespa quotes, historical OHLCV, dividends, and fundamentals.
- [13F Insight](https://13finsight.com/) - Track institutional investor 13F holdings with AI-powered analysis, position change alerts, and filing summaries.
- [Earnings Feed](https://earningsfeed.com/api) - Real-time SEC filings, insider trades, and institutional holdings API.
- [Financial Data](https://financialdata.net/) - Stock Market and Financial Data API.
- [Frostbyte](https://agent-gateway-kappa.vercel.app) - Real-time crypto prices for 500+ tokens via REST API with free tier, DeFi swap routing and portfolio tracking.
- [SaxoOpenAPI](https://www.developer.saxo/) - Saxo Bank financial data API.
- [RTPR](https://rtpr.io) - Real-time press release API delivering news from Business Wire, PR Newswire, and GlobeNewswire with sub-500ms latency. REST and WebSocket APIs for financial applications. Python and Node.js SDKs available.
- [Nasdaq Data Link](https://data.nasdaq.com/tools/full-list) - Financial data API with support for R, Python, Excel, Ruby, and many other languages (formerly Quandl).
- [Parsec](https://parsecfinance.com) - Prediction market API with Python SDK for normalized data and execution across 5 prediction market exchanges. Free tier: 10K requests/month.
- [Portfolio Optimizer](https://portfoliooptimizer.io/) - Portfolio Optimizer is a Web API for portfolio analysis and optimization.
- [Reddit WallstreetBets API](https://dashboard.nbshare.io/apps/reddit/api/) - Provides daily top 50 stocks from reddit (subreddit) Wallstreetbets and their sentiments via the API.
- [System R](https://agents.systemr.ai) - AI-native risk intelligence API for trading agents. Position sizing, risk validation, and system health in one call.
- [Telonex](https://telonex.io) - Tick-level prediction market data (trades, quotes, orderbooks, on-chain fills) via REST API and Python SDK.
- [ValueRay](https://www.valueray.com/api) - Technical, quantitative and sentiment data for stocks and ETFs with risk metrics, peer percentiles and market regime signals. Optimized for AI/LLM agents.
- [VertData](https://vertdata.com) - Institutional-grade financial intelligence platform. Track 43K+ congressional trades (STOCK Act), SEC insider Form 4 filings, 25 superinvestor 13F portfolios, CFTC futures positioning, ARK ETF holdings, and short interest — all scored by AI for signal strength.
- [KeepRule](https://keeprule.com/) - Curated library of decision-making principles and investment wisdom from masters like Buffett and Munger, featuring mental models for better investment thinking.
- [ML-Quant](https://www.ml-quant.com/) - Top Quant resources like ArXiv (sanity), SSRN, RePec, Journals, Podcasts, Videos, and Blogs.

## Related Lists

- [awesome-sec-filings](https://github.com/vibeyclaw/awesome-sec-filings) - A curated list of tools, data sources, libraries, and resources for working with SEC filings (13F, 10-K, 10-Q, 8-K).
- [CONVEXFI](https://github.com/convexfi) - Official GitHub organization for the convex research group at the Hong Kong University of Science and Technology (HKUST).
