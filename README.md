# awesome-quant
A curated list of insanely awesome libraries, packages and resources for Quants (Quantitative Finance)

## Languages

- [Python](#python)
- [R](#r)
- [Julia](#julia)
- [Java](#java)
- [Haskell](#haskell)
- [Scala](#scala)
- [Frameworks](#frameworks) - frameworks that support different languages
- [Reproducing Works](#reproducing-works) - repositories that reproduce books and papers results or implement examples

##Python

### Numerical Libraries & Data Structures

- [numpy](http://www.numpy.org) - NumPy is the fundamental package for scientific computing with Python.
- [scipy](https://www.scipy.org) - SciPy (pronounced “Sigh Pie”) is a Python-based ecosystem of open-source software for mathematics, science, and engineering.
- [pandas](http://pandas.pydata.org) - pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.

### Financial Instruments

- [PyQL](https://github.com/enthought/pyql) - QuantLib's Python port
- [pyfin](https://github.com/opendoor-labs/pyfin) - Basic options pricing in Python
- [vollib](https://github.com/vollib/vollib) - vollib is a python library for calculating option prices, implied volatility and greeks.
- [QuantPy](https://github.com/jsmidt/QuantPy) - A framework for quantitative finance In python.

### Trading

- [TA-Lib](http://ta-lib.org) - perform technical analysis of financial market data
- [trade](https://github.com/rochars/trade) - trade is a Python framework for the development of financial applications.
- [zipline](http://www.zipline.io) - Pythonic algorithmic trading library
- [QuantSoftware Toolkit](http://wiki.quantsoftware.org/index.php?title=QuantSoftware_ToolKit) - Python-based open source software framework designed to support portfolio construction and management.
- [quantitative](https://github.com/jeffrey-liang/quantitative) - Quantitative finance, and backtesting library

### Risk Analysis

- Python
	- [pyfolio](https://github.com/quantopian/pyfolio) - Portfolio and risk analytics in Python
	- [qrisk](https://github.com/quantopian/qrisk) - Common financial risk and performance metrics.

### Time Series

- [ARCH](https://github.com/bashtage/arch) - ARCH models in Python
- [statsmodels](http://statsmodels.sourceforge.net) - Python module that allows users to explore data, estimate statistical models, and perform statistical tests.

### Calendars

- [tradingcalendar](https://github.com/quantopian/tradingcalendar) - Stock Exchange Trading Calendar
- [bizdays](https://github.com/wilsonfreitas/python-bizdays) - Business days calculations and utilities

## R

### Numerical Libraries & Data Structures

- [xts](https://cran.r-project.org/web/packages/xts/index.html) - eXtensible Time Series: Provide for uniform handling of R's different time-based data classes by extending zoo, maximizing native format information preservation and allowing for user level customization and extension, while simplifying cross-class interoperability.
- [data.table](https://cran.r-project.org/web/packages/data.table/index.html) - Extension of data.frame: Fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins, fast add/modify/delete of columns by group using no copies at all, list columns and a fast file reader (fread). Offers a natural and flexible syntax, for faster development.

### Financial Instruments

- [RQuantLib](http://dirk.eddelbuettel.com/code/rquantlib.html) - RQuantLib connects GNU R with QuantLib.
- [quantmod](https://cran.r-project.org/web/packages/quantmod/index.html) - Quantitative Financial Modelling Framework
- [Rmetrics](https://www.rmetrics.org) - The premier open source software solution for teaching and training quantitative finance
	- [fAsianOptions](https://cran.r-project.org/web/packages/fAsianOptions/index.html) - EBM and Asian Option Valuation
	- [fAssets](https://cran.r-project.org/web/packages/fAssets/index.html) - Analysing and Modelling Financial Assets
	- [fBasics](https://cran.r-project.org/web/packages/fBasics/index.html) - Markets and Basic Statistics
	- [fBonds](https://cran.r-project.org/web/packages/fBonds/index.html) - Bonds and Interest Rate Models
	- [fExoticOptions](https://cran.r-project.org/web/packages/fExoticOptions/index.html) - Exotic Option Valuation
	- [fOptions](https://cran.r-project.org/web/packages/fOptions/index.html) - Pricing and Evaluating Basic Options
	- [fPortfolio](https://cran.r-project.org/web/packages/fPortfolio/index.html) - Portfolio Selection and Optimization
- [portfolio](https://cran.r-project.org/web/packages/portfolio/index.html) - Analysing equity portfolios
- [portfolioSim](https://cran.r-project.org/web/packages/portfolioSim/index.html) - Framework for simulating equity portfolio strategies
- [stockPortfolio](https://cran.r-project.org/web/packages/stockPortfolio/index.html) - Build stock models and analyze stock portfolios
- [financial](https://cran.r-project.org/web/packages/financial/index.html) - Time value of money, cash flows and other financial functions.
- [sde](https://cran.r-project.org/web/packages/sde/index.html) - Simulation and Inference for Stochastic Differential Equations
- [termstrc](https://cran.r-project.org/web/packages/termstrc/index.html) - Zero-coupon Yield Curve Estimation
- [YieldCurve](https://cran.r-project.org/web/packages/YieldCurve/index.html) - Modelling and estimation of the yield curve
- [SmithWilsonYieldCurve](https://cran.r-project.org/web/packages/SmithWilsonYieldCurve/index.html) - Constructs a yield curve by the Smith-Wilson method from a table of LIBOR and SWAP rates
- [ycinterextra](https://cran.r-project.org/web/packages/ycinterextra/index.html) - Yield curve or zero-coupon prices interpolation and extrapolation
- [opefimor](https://cran.r-project.org/web/packages/opefimor/index.html) - Option Pricing and Estimation of Financial Models in R
- [maRketSim](https://cran.r-project.org/web/packages/maRketSim/index.html) - Market simulator for R
- [AmericanCallOpt](https://cran.r-project.org/web/packages/AmericanCallOpt/index.html) - This package includes pricing function for selected American call options with underlying assets that generate payouts
- [VarSwapPrice](https://cran.r-project.org/web/packages/VarSwapPrice/index.html) - Pricing a variance swap on an equity index
- [RND](https://cran.r-project.org/web/packages/RND/index.html) - Risk Neutral Density Extraction Package
- [LSMonteCarlo](https://cran.r-project.org/web/packages/LSMonteCarlo/index.html) - American options pricing with Least Squares Monte Carlo method
- [OptHedging](https://cran.r-project.org/web/packages/OptHedging/index.html) - Estimation of value and hedging strategy of call and put options
- [tvm](https://cran.r-project.org/web/packages/tvm/index.html) - Time Value of Money Functions
- [OptionPricing](https://cran.r-project.org/web/packages/OptionPricing/index.html) - Option Pricing with Efficient Simulation Algorithms
- [credule](https://cran.r-project.org/web/packages/credule/index.html) - Credit Default Swap Functions
- [derivmkts](https://cran.r-project.org/web/packages/derivmkts/index.html) - Functions and R Code to Accompany Derivatives Markets
- [FinCal](https://github.com/felixfan/FinCal) - Package for time value of money calculation, time series analysis and computational finance
- [r-quant](https://github.com/artyyouth/r-quant) - R code for quantitative analysis in finance

### Trading

- [TA-Lib](http://ta-lib.org) - perform technical analysis of financial market data
- [backtest](https://cran.r-project.org/web/packages/backtest/index.html) - Exploring Portfolio-Based Conjectures About Financial Instruments
- [pa](https://cran.r-project.org/web/packages/pa/index.html) - Performance Attribution for Equity Portfolios
- [TTR](https://cran.r-project.org/web/packages/TTR/index.html) - Technical Trading Rules

### Risk Analysis

- [PerformanceAnalytics](https://cran.r-project.org/web/packages/PerformanceAnalytics/index.html) - Econometric tools for performance and risk analysis

### Time Series

### Calendars

- [RQuantLib](http://dirk.eddelbuettel.com/code/rquantlib.html)
- [timeDate](https://cran.r-project.org/web/packages/timeDate/index.html) - Chronological and Calendar Objects
- [bizdays](https://cran.r-project.org/web/packages/bizdays/index.html) - Business days calculations and utilities

## Julia

- [QuantLib.jl](https://github.com/pazzo83/QuantLib.jl) - Quantlib implementation in pure Julia.
- [FinancialMarkets.jl](https://github.com/imanuelcostigan/FinancialMarkets.jl) - Describe and model financial markets objects using Julia
- [Ito.jl](https://github.com/aviks/Ito.jl) - A Julia package for quantitative finance

## Java

- [JQuantLib](http://www.jquantlib.org) - JQuantLib is a free, open-source, comprehensive framework for quantitative finance, written in 100% Java.
- [finmat.net](http://finmath.net) - Java library with algorithms and methodologies related to mathematical finance.
- [quantcomponents](https://github.com/lsgro/quantcomponents) - Free Java components for Quantitative Finance and Algorithmic Trading

## Haskell

- [quantfin](https://github.com/boundedvariation/quantfin) - quant finance in pure haskell
- [hqfl](https://github.com/cokleisli/hqfl) - Haskell Quantitative Finance Library

## Scala

- [QuantScale](https://github.com/choucrifahed/quantscale) - Scala Quantitative Finance Library

## Frameworks

- [QuantLib](http://www.quantlib.org) - The QuantLib project is aimed at providing a comprehensive software framework for quantitative finance.
	- [JQuantLib](http://www.jquantlib.org) - Java port
	- [RQuantLib](http://dirk.eddelbuettel.com/code/rquantlib.html) - R port
	- [QuantLibAddin](http://quantlibaddin.org/) - Excel support
	- [QuantLibXL](http://quantlibxl.org/) - Excel support
	- [QLNet](https://github.com/amaggiulli/qlnet) - .Net port
	- [PyQL](https://github.com/enthought/pyql) - Python port
	- [QuantLib.jl](https://github.com/pazzo83/QuantLib.jl) - Julia port
- [TA-Lib](http://ta-lib.org) - perform technical analysis of financial market data


## Reproducing Works

- [Derman Papers](https://github.com/MarcosCarreira/DermanPapers) - Notebooks that replicate original quantitative finance papers from Emanuel Derman.
- [volatility-trading](https://github.com/jasonstrimpel/volatility-trading) - A complete set of volatility estimators based on Euan Sinclair's Volatility Trading.
- [quant](https://github.com/paulperry/quant) -  Quantitative Finance and Algorithmic Trading exhaust; mostly ipython notebooks based on Quantopian, Zipline, or Pandas.

