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
- [Market Data & Data Sources](#market-data--data-sources)
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
- [scipy](https://www.scipy.org) - `Python` - SciPy (pronounced “Sigh Pie”) is a Python-based ecosystem of open-source software for mathematics, science, and engineering. [GitHub](https://gith[...]
- [pandas](https://pandas.pydata.org) - `Python` - pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python pro[...]
- [polars](https://docs.pola.rs/) - `Python` - Polars is a blazingly fast DataFrame library for manipulating structured data. [GitHub](https://github.com/pola-rs/polars)
- [quantdsl](https://github.com/johnbywater/quantdsl) - `Python` - Domain specific language for quantitative analytics in finance and trading.
- [statistics](https://docs.python.org/3/library/statistics.html) - `Python` - Builtin Python library for all basic statistical calculations.
- [sympy](https://www.sympy.org/) - `Python` - SymPy is a Python library for symbolic mathematics. [GitHub](https://github.com/sympy/sympy)
- [pymc3](https://docs.pymc.io/) - `Python` - Probabilistic Programming in Python: Bayesian Modeling and Probabilistic Machine Learning with Theano. [GitHub](https://github.com/pymc-devs/pymc)
- [modelx](https://docs.modelx.io/) - `Python` - Python reimagination of spreadsheets as formula-centric objects that are interoperable with pandas. [GitHub](https://github.com/fumitoh/modelx)
- [ArcticDB](https://github.com/man-group/ArcticDB) - `Python` - High performance datastore for time series and tick data.
- [CRNG](https://github.com/brotto/crng) - `Python` - Contingency Random Number Generator that produces random numbers with real financial market statistical signatures (fat tails, volatility clus[...]
- [xts](https://github.com/joshuaulrich/xts) - `R` - eXtensible Time Series: Provide for uniform handling of R's different time-based data classes by extending zoo, maximizing native format inform[...]
- [data.table](https://github.com/Rdatatable/data.table) - `R` - Extension of data.frame: Fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins, fast add/modify/delete of columns [...]
- [sparseEigen](https://github.com/dppalomar/sparseEigen) - `R` - Sparse principal component analysis.
- [TSdbi](http://tsdbi.r-forge.r-project.org/) - `R` - Provides a common interface to time series databases.
- [tseries](https://cran.r-project.org/web/packages/tseries/index.html) - `R` - Time Series Analysis and Computational Finance.
- [zoo](https://cran.r-project.org/web/packages/zoo/index.html) - `R` - S3 Infrastructure for Regular and Irregular Time Series (Z's Ordered Observations).
- [tis](https://cran.r-project.org/web/packages/tis/index.html) - `R` - Functions and S3 classes for time indexes and time indexed series, which are compatible with FAME frequencies.
- [tfplot](https://cran.r-project.org/web/packages/tfplot/index.html) - `R` - Utilities for simple manipulation and quick plotting of time series data.
- [tframe](https://cran.r-project.org/web/packages/tframe/index.html) - `R` - A kernel of functions for programming time series methods in a way that is relatively independently of the representat[...]
- [Temporal.jl](https://github.com/dysonance/Temporal.jl) - `Julia` - Flexible and efficient time series class & methods.
- [DataFrames.jl](https://github.com/JuliaData/DataFrames.jl) - `Julia` - In-memory tabular data in Julia.
- [TSFrames.jl](https://github.com/xKDR/TSFrames.jl) - `Julia` - Handle timeseries data on top of the powerful and mature DataFrames.jl.
- [TimeArrays.jl](https://github.com/bhftbootcamp/TimeArrays.jl) - `Julia` - Time series handling for Julia.

## Financial Instruments & Pricing

- [PyQL](https://github.com/enthought/pyql) - `Python` - QuantLib's Python port.
- [pyfin](https://github.com/opendoor-labs/pyfin) - `Python` - Basic options pricing in Python. *ARCHIVED*.
- [vollib](https://github.com/vollib/vollib) - `Python` - vollib is a python library for calculating option prices, implied volatility and greeks.
- [py_vollib](https://github.com/vollib/py_vollib) - `Python` - vollib Python implementation.
- [StochVolModels](https://github.com/ArturSepp/StochVolModels) - `Python` - Pricing analytics and Monte Carlo simulation for stochastic volatility models, including the log-normal SV model and th[...]
- [QuantPy](https://github.com/jsmidt/QuantPy) - `Python` - A framework for quantitative finance In python.
- [Finance-Python](https://github.com/alpha-miner/Finance-Python) - `Python` - Python tools for Finance.
- [ffn](https://github.com/pmorissette/ffn) - `Python` - A financial function library for Python.
- [pynance](https://github.com/GriffinAustin/pynance) - `Python` - Lightweight Python library for assembling and analyzing financial data.
- [tia](https://github.com/bpsmith/tia) - `Python` - Toolkit for integration and analysis.
- [pysabr](https://github.com/ynouri/pysabr) - `Python` - SABR model Python implementation.
- [FinancePy](https://github.com/domokane/FinancePy) - `Python` - A Python Finance Library that focuses on the pricing and risk-management of Financial Derivatives, including fixed-income, equity,[...]
- [gs-quant](https://github.com/goldmansachs/gs-quant) - `Python` - Python toolkit for quantitative finance.
- [willowtree](https://github.com/federicomariamassari/willowtree) - `Python` - Robust and flexible Python implementation of the willow tree lattice for derivatives pricing.
- [financial-engineering](https://github.com/federicomariamassari/financial-engineering) - `Python` - Applications of Monte Carlo methods to financial engineering projects, in Python.
- [optlib](https://github.com/dbrojas/optlib) - `Python` - A library for financial options pricing written in Python.
- [tf-quant-finance](https://github.com/google/tf-quant-finance) - `Python` - High-performance TensorFlow library for quantitative finance.
- [Q-Fin](https://github.com/RomanMichaelPaolucci/Q-Fin) - `Python` - A Python library for mathematical finance.
- [Quantsbin](https://github.com/quantsbin/Quantsbin) - `Python` - Tools for pricing and plotting of vanilla option prices, greeks and various other analysis around them.
- [finoptions](https://github.com/bbcho/finoptions-dev) - `Python` - Complete python implementation of R package fOptions with partial implementation of fExoticOptions for pricing various options.
- [pypme](https://github.com/ymyke/pypme) - `Python` - PME (Public Market Equivalent) calculation.
- [AbsBox](https://github.com/yellowbean/AbsBox) - `Python` - A Python based library to model cashflow for structured product like Asset-backed securities (ABS) and Mortgage-backed securities (MBS[...]
- [mortgagemath](https://github.com/murraystokely/mortgagemath) - `Python` - Cent-accurate mortgage amortization schedules with Decimal arithmetic and published-source validation across six countr[...]
- [Intrinsic-Value-Calculator](https://github.com/akashaero/Intrinsic-Value-Calculator) - `Python` - A Python tool for quick calculations of a stock's fair value using Discounted Cash Flow analysi[...]
- [Kelly-Criterion](https://github.com/deltaray-io/kelly-criterion) - `Python` - Kelly Criterion implemented in Python to size portfolios based on J. L. Kelly Jr's formula.
- [rateslib](https://github.com/attack68/rateslib) - `Python` - A fixed income library for pricing bonds and bond futures, and derivatives such as IRS, cross-currency and FX swaps.
- [fypy](https://github.com/jkirkby3/fypy) - `Python` - Vanilla and exotic option pricing library to support quantitative R&D. Focus on pricing interesting/useful models and contracts (including a[...]
- [Pyderivatives](https://github.com/Julian-Beatty/Pyderivatives) - `Python` - Toolkit for option pricing, implied volatility surfaces, risk-neutral densities, and pricing kernel surfaces with sup[...]
- [quantra](https://github.com/joseprupi/quantraserver) - `Python` - High-performance pricing engine built on QuantLib. It exposes QuantLib's functionality through gRPC and REST APIs, enabling dis[...]
- [optionlab](https://github.com/rgaveiga/optionlab) - `Python` - A Python library for evaluating option trading strategies.
- [flashalpha](https://github.com/FlashAlpha-lab/flashalpha-python) - `Python` - Python client for the FlashAlpha options analytics API.
- [QuantOracle](https://github.com/QuantOracledev/quantoracle) - `Python` - Free quant finance API with 63 deterministic endpoints + 15 free interactive calculators at [quantoracle.dev](https://qu[...]
- [implied-expectations](https://github.com/Keenan-ux/implied-expectations) - `Python` - Reverse DCF that solves for the revenue growth, duration, and operating margin a stock price implies, from [...]
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
- [SmithWilsonYieldCurve](https://github.com/alexiosg/SmithWilsonYieldCurve) - `R` - Constructs a yield curve by the Smith-Wilson method from a table of LIBOR and SWAP rate[...]
- [AmericanCallOpt](https://cran.r-project.org/web/packages/AmericanCallOpt/index.html) - `R` - This package includes pricing function for selected American call options with underlying assets th[...]
- [VarSwapPrice](https://cran.r-project.org/web/packages/VarSwapPrice/index.html) - `R` - Pricing a variance swap on an equity index.
- [RND](https://github.com/wol-fi/direct_vola) - `R` - Demo code for direct Black-Scholes implied-volatility calculation from normalized call prices via the inverse-Gaussian quan[...]
- [LSMonteCarlo](https://github.com/enricoschumann/LSMonteCarlo) - `R` - American options pricing with Least Squares Monte Carlo method.
- [OptHedging](https://github.com/attack68/OptHedging) - `R` - Estimation of value and hedging strategy of call and put options.
- [tvm](https://cran.r-project.org/web/packages/tvm/index.html) - `R` - Time Value of Money Functions.
- [OptionPricing](https://github.com/lingyixu/OptionPricing) - `R` - Option Pricing with Efficient Simulation Algorithms.
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
- [finmath.net](http://finmath.net) - `Java` - Java library with algorithms and methodologies related to mathematical finance.
- [quantcomponents](https://github.com/lsgro/quantcomponents) - `Java` - Free Java components for Quantitative Finance.
- [DRIP](https://lakshmidrip.github.io/DRIP) - `Java` - Fixed Income, Asset Allocation, Transaction Cost Analysis, XVA Metrics Libraries.
- [finance.js](https://github.com/ebradyjobory/finance.js) - `JavaScript` - A JavaScript library for common financial calculations.
- [hagan-sabr](https://github.com/moshejs/hagan-sabr) - `TypeScript` - SABR stochastic-volatility model (Hagan 2002 lognormal/normal expansions, Obłój correction, smile calibration); zero depen[...]
- [svi-vol-surface](https://github.com/moshejs/svi-vol-surface) - `TypeScript` - Gatheral SVI volatility surface (raw/natural/jump-wings), butterfly and calendar arbitrage checks, slice calibrati[...]
- [compounded-sofr](https://github.com/moshejs/compounded-sofr) - `TypeScript` - Gatheral SVI volatility surface (raw/natural/jump-wings), butterfly and calendar arbitrage checks, slice calibrati[...]
- [day-count-conventions](https://github.com/moshejs/day-count) - `TypeScript` - ISDA 2006 day-count conventions (30/360 family, ACT/360, ACT/365F, ACT/ACT ISDA and ICMA); zero dependencies.
- [tips-index-ratio](https://github.com/moshejs/tips-index-ratio) - `TypeScript` - US TIPS inflation math per 31 CFR 356 Appendix B (reference-CPI interpolation, index ratios); reproduces Treasur[...]
- [32nds](https://github.com/moshejs/32nds) - `TypeScript` - US Treasury price quote math: parse and format 32nds quotes (105/246 s[...]

## Technical Indicators

- [pandas_talib](https://github.com/femtotrader/pandas_talib) - `Python` - A Python Pandas implementation of technical analysis indicators.
- [finta](https://github.com/peerchemist/finta) - `Python` - Common financial technical analysis indicators implemented in Pandas.
- [Tulipy](https://github.com/cirla/tulipy) - `Python` - Financial Technical Analysis Indicator Library (Python bindings for [tulipindicators](https://github.com/TulipCharts/tulipindicators)).
- [lppls](https://github.com/Boulder-Investment-Technologies/lppls) - `Python` - A Python module for fitting the [Log-Periodic Power Law Singularity (LPPLS)](https://en.wikipedia.org/wiki/Didier_[...]
- [talipp](https://github.com/nardew/talipp) - `Python` - Incremental technical analysis library for Python.
- [streaming_indicators](https://github.com/mr-easy/streaming_indicators) - `Python` - A python library for computing technical analysis indicators on streaming data.
- [TA-Lib](https://github.com/mrjbq7/ta-lib) - `Python` - Python wrapper for TA-Lib (<http://ta-lib.org/>).
- [ta](https://github.com/bukosabino/ta) - `Python` - Technical Analysis Library using Pandas (Python).
- [bta-lib](https://github.com/mementum/bta-lib) - `Python` - Linter for mechanical trading-rule conditions: replays every condition over historical bars to catch look-ahead levels, dead branche[...]
- [TuneTA](https://github.com/jmrichardson/tuneta) - `Python` - TuneTA optimizes technical indicators using a distance correlation measure to a user defined target feature such as next day return[...]
- [TTR](https://github.com/joshuaulrich/TTR) - `R` - Technical Trading Rules.
- [TALib.jl](https://github.com/femtotrader/TALib.jl) - `Julia` - A Julia wrapper for TA-Lib.
- [Indicators.jl](https://github.com/dysonance/Indicators.jl) - `Julia` - Financial market technical analysis & indicators on top of Temporal.
- [TechnicalIndicatorCharts.jl](https://github.com/g-gundam/TechnicalIndicatorCharts.jl) - `Julia` - Visualize OnlineTechnicalIndicators.jl using LightweightCharts.jl.
- [MarketTechnicals.jl](https://github.com/JuliaQuant/MarketTechnicals.jl) - `Julia` - Financial market technical analysis on top of TimeSeries.
- [OnlineTechnicalIndicators.jl](https://github.com/femtotrader/OnlineTechnicalIndicators.jl) - `Julia` - Incremental online technical indicators.
- [ta4j](https://github.com/ta4j/ta4j) - `Java` - TA library for Java.
- [IndicatorTS](https://github.com/cinar/indicatorts) - `JavaScript` - Indicator is a TypeScript module providing various stock technical analysis indicators, strategies, and a backtest framework[...]
- [chart-patterns](https://github.com/focus1691/chart-patterns) - `JavaScript` - Technical analysis library for Market Profile, Volume Profile, Stacked Imbalances and High Volume Node indicators.
- [orderflow](https://github.com/focus1691/orderflow) - `JavaScript` - Orderflow trade aggregator for building Footprint Candles from exchange websocket data.
- [IndicatorGo](https://runmat.org) - `Golang` - IndicatorGo is a Golang module providing various stock technical analysis indicators, strategies, and a backtest framework for tra[...]

## Trading & Backtesting
- [rulelint](https://github.com/momoddo/rulelint) - `Python` - Linter for mechanical trading-rule conditions: replays every condition over historical bars to catch look-ahead levels, dead branche[...]
- [FAIG](https://github.com/tg12/FAIG) - `Python` - Fully automated trading bot for the IG Index platform (spread betting and CFDs), supporting demo and live accounts.
- [quantify](https://github.com/Zhanghanser/quantify) - `Python` - Binance-style trading terminal with multi-strategy backtesting and a real-time, signal-only decision desk for crypto, A-shares, [...]
- [purgedcv](https://github.com/eslazarev/purged-cross-validation) - `Python` - scikit-learn-compatible purged, group-purged, and combinatorial purged (CPCV) cross-validation, walk-forward splitt[...]
- [AlgoVault](https://github.com/AlgoVaultLabs/crypto-quant-signal-mcp) - `TypeScript` - MCP server returning composite crypto trade verdicts (direction, confidence, regime) across 5 perpetua[...]
- [alpha-forge-mcp](https://github.com/alforge-labs/alpha-forge-mcp) - `Python` - MCP server wrapping the AlphaForge CLI for AI-agent-native backtesting, Optuna TPE optimization, and walk-forward[...]
- [capitalcom-cli](https://github.com/SimonTarara62/capitalcom-cli) - `Python` - Unofficial CLI and async SDK for the Capital.com broker API: market data, guarded order execution, and real-time s[...]
- [Inalpha](https://github.com/mirror29/inalpha) - `Python` `TypeScript` - Conversational multi-agent quant framework where agents rank currently-effective factors for entry timing (time-series r[...]
- [income-desk](https://github.com/nitinblue/income-desk) - `Python` - Systematic options trading intelligence for small accounts with desk-based portfolio management, pre-trade validation, and m[...]
- [mx-trader-bridge](https://github.com/27dream/mx-trader-bridge) - `Python` - AI auto-trading bridge for East Money's miaoxiang (妙想) China A-share simulation platform; BYOK multi-LLM (OpenAI[...]

## Portfolio Optimization & Risk Analysis

- [Multi-Axis Robust Portfolio Optimization](https://github.com/Viraj-Nigwekar/multi-axis-robust-portfolio-optimization) - `Python` `Portfolio Optimization` `Robust Optimization` - Portfolio optimization framework combining covariance shrinkage, bootstrap aggregation, and parametric stress testing for robust asset allocation.
- [AutoHypothesis](https://github.com/arteemg/AutoHypothesis) - `Python` - An agentic framework that mimics the real quant trading pipeline to find alpha: economic hypothesis, in-sample iteration[...]
- [skfolio](https://github.com/skfolio/skfolio) - `Python` - Python library for portfolio optimization built on top of scikit-learn. It provides a unified interface and sklearn compatible tools t[...]
- [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) - `Python` - Financial portfolio optimization in python, including classical efficient frontier and advanced methods.
- [factorlasso](https://github.com/ArturSepp/factorlasso) - `Python` - Sparse multi-asset factor models with cell-level sign constraints, prior-centred shrinkage, and hierarchical clustering grou[...]
- [OptimalPortfolios](https://github.com/ArturSepp/OptimalPortfolios) - `Python` - Optimisation analytics for constructing and backtesting optimal multi-asset portfolios: covariance estimation, r[...]
- [Eiten](https://github.com/tradytics/eiten) - `Python` - Eiten is an open source toolkit by Tradytics that implements various statistical and algorithmic investing strategies such as Eigen Port[...]
- [riskparity.py](https://github.com/dppalomar/riskparity.py) - `Python` - fast and scalable design of risk parity portfolios with TensorFlow 2.0.
- [mlfinlab](https://github.com/hudson-and-thames/mlfinlab) - `Python` - Implementations regarding "Advances in Financial Machine Learning" by Marcos Lopez de Prado. (Feature Engineering, Financi[...]
- [DeepDow](https://github.com/jankrepl/deepdow) - `Python` - Portfolio optimization with deep learning.
- [QuantLibRisks](https://github.com/auto-differentiation/QuantLib-Risks-Py) - `Python` - Fast risks with QuantLib.
- [XAD](https://github.com/auto-differentiation/xad-py) - `Python` - Automatic Differentation (AAD) Library.
- [pyfolio](https://github.com/quantopian/pyfolio) - `Python` - Portfolio and risk analytics in Python.
- [etfray](https://github.com/alwank/etfray) - `Python` - Terminal-based ETF research and portfolio analytics application for holdings, exposure, concentration, margin, and risk workflows.
- [empyrical](https://github.com/quantopian/empyrical) - `Python` - Common financial risk and performance metrics.
- [fecon235](https://github.com/rsvp/fecon235) - `Python` - Computational tools for financial economics include: Gaussian Mixture model of leptokurtotic risk, adaptive Boltzmann portfolios.
- [finance](https://pypi.org/project/finance/) - `Python` - Financial Risk Calculations. Optimized for ease of use through class construction and operator overload.
- [qfrm](https://pypi.org/project/qfrm/) - `Python` - Quantitative Financial Risk Management: awesome OOP tools for measuring, managing and visualizing risk of financial instruments and portfolio[...]
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
- [curistat](https://github.com/moxiespirit/MyClone/tree/main/volatility_platform) - `Python` - Futures volatility forecasting platform for ES/NQ. Proprietary CVN rating (1-10), regime detection [...]
- [Prop Trader Compass](https://otto-ships.github.io/prop-trader-compass/) - `Python` - Interactive risk and payout calculator for Futures and CFD traders; features one-time fee firm comparisons.
- [riskkit](https://github.com/HasibVortex369/riskkit) - `Python` - Framework-agnostic risk-management toolkit for systematic trading — position sizing, drawdown control, a composable stop engi[...]
- [portfolio](https://github.com/dgerlanc/portfolio) - `R` - Analysing equity portfolios.
- [sparseIndexTracking](https://github.com/dppalomar/sparseIndexTracking) - `R` - Portfolio design to track an index.
- [riskParityPortfolio](https://github.com/dppalomar/riskParityPortfolio) - `R` - Blazingly fast design of risk parity portfolios.
- [PortfolioAnalytics](https://github.com/braverock/PortfolioAnalytics) - `R` - Portfolio Analysis, Including Numerical Methods for Optimizationof Portfolios.
- [PerformanceAnalytics](https://github.com/braverock/PerformanceAnalytics) - `R` - Econometric tools for performance and risk analysis.
- [OnlinePortfolioAnalytics.jl](https://github.com/femtotrader/OnlinePortfolioAnalytics.jl) - `Julia` - A Julia quantitative portfolio analytics (risk / performance) via online algorithms.
- [RiskPerf.jl](https://github.com/rbeeli/RiskPerf.jl) - `Julia` - Quantitative risk and performance analysis package for financial time series powered by the Julia language.
- [portfolio-allocation](https://github.com/lequant40/portfolio_allocation_js) - `JavaScript` - PortfolioAllocation is a JavaScript library designed to help constructing financial portfolios made[...]
- [Ghostfolio](https://github.com/ghostfolio/ghostfolio) - `JavaScript` - Wealth management software to keep track of financial assets like stocks, ETFs or cryptocurrencies and make solid, data-d[...]
- [rebalance](https://github.com/cjroth/rebalance) - `JavaScript` - Interactive portfolio rebalancing tool that imports brokerage CSV data, sets target allocations, and generates trade instructio[...]

## Factor Analysis

- [Alpha Skills](https://github.com/VernonOY/alpha-skills) - `Python` - AI skills for quantitative factor research: discover, evaluate, mine, backtest, and monitor factors through any AI coding a[...]
- [alphalens](https://github.com/quantopian/alphalens) - `Python` - Performance analysis of predictive alpha factors.
- [alphalens-reloaded](https://github.com/stefan-jansen/alphalens-reloaded) - `Python` - Performance analysis of predictive (alpha) stock factors.
- [Spectre](https://github.com/Heerozh/spectre) - `Python` - GPU-accelerated Factors analysis library and Backtester.
- [ml-quant-trading](https://github.com/initial-d/ml-quant-trading) - `Python` - PyTorch research stack for multi-factor analysis, bias correction, portfolio optimization, and reproducible backte[...]

... (file continues unchanged)
