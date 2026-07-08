
# Awesome Quant [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

一份精心挑选的中文Quant相关资源索引。

## 目录

*  [数据源](#数据源)
*  [数据库](#数据库)
*  [量化交易平台](#量化交易平台)
*   [策略](#策略)
*  [回测](#回测)
*  [交易API](#交易api)
*  [编程](#编程)
    * [Python](#python)
    * [R](#r)
    * [C++](#c)
    * [Julia](#julia)
*  [论坛](#论坛)
*  [书籍](#书籍)
*  [论文](#论文)
*  [政策](#政策)
* [值得关注的信息源](#值得关注的信息源)
*  [其他Quant资源索引](#其他quant资源索引)

## 数据源
* [TuShare](http://tushare.org/)  - 中文财经数据接口包
* [Quandl](https://www.quandl.com/) - 国际金融和经济数据
* [Wind资讯-经济数据库](http://www.wind.com.cn/NewSite/edb.html) - 收费
* [锐思数据 - 首页](http://www.resset.cn/) - 收费
* [国泰安数据服务中心](http://www.gtarsc.com/Home) - 收费
* [恒生API](https://open.hscloud.cn/cloud/open/apilibrary/queryLibraryMenu.html?parent_id=100313&menu_id=100307) - 收费
* [Bloomberg API](https://www.bloomberglabs.com/api/libraries/)  - 收费
* [数库金融数据和深度分析API服务](http://developer.chinascope.com/) - 收费
* [Historical Data Sources](http://quantpedia.com/Links/HistoricalData) - 一个数据源索引
* [Python通达信数据接口](https://github.com/rainx/pytdx) - 免费通达信数据源
* [fooltrader](https://github.com/foolcage/fooltrader) - 大数据开源量化项目,自己维护了一个爬取整合的全市场数据源
* [zvt](https://github.com/zvtvz/zvt) - ZVT是在fooltrader的基础上重新思考后编写的量化项目，其包含可扩展的数据recorder，api，因子计算，选股，回测，定位为中低频 多级别 多标的 全市场分析和交易框架。
* [JoinQuant/jqdatasdk](https://github.com/JoinQuant/jqdatasdk) - jqdatasdk是提供给用户获取聚宽金融数据的SDK
* [米筐科技的RQData数据接口](https://www.ricequant.com/introduce_rqdata) - 收费
* [AkShare](https://github.com/jindaxiang/akshare) - 免费开源财经数据接口库，目前包含中文领域最全的数据接口
* [Financial Data](https://financialdata.net/) - 股票市场和财务数据
* [FXMacroData](https://fxmacrodata.com) - 实时外汇宏观经济数据 API，提供 18 种货币的央行公告、利率、通胀、就业和 GDP 数据。支持 MCP 服务器和 OAuth。[GitHub](https://github.com/fxmacrodata/fxmacrodata) | [PyPI](https://pypi.org/project/fxmacrodata/)
* [Adanos Market Sentiment API](https://adanos.org/) - 股票市场情绪 API，结合 Reddit、X/Twitter 和 Polymarket 信号，提供 trending tickers、buzz scores 和情绪指标。
* [13F Insight](https://13finsight.com) - AI 驱动的美国机构持仓追踪平台，覆盖 380K+ 13F 持仓报告、480K+ 13D/G 激进投资者申报和 437万+ Form 4 内部人交易数据，内嵌 AI Agent 支持自然语言查询。
* [finlight](https://finlight.me/) - 实时财经新闻 API，聚焦全球金融、地缘政治与市场新闻，提供 REST 和 WebSocket 接口，内置实体识别与情绪分析。[GitHub](https://github.com/jubeiargh/finlight-client-py) | [PyPI](https://pypi.org/project/finlight-client/)
* [stock-analysis](https://github.com/AdvancingTitans/stock-analysis) - 面向 A股、港股、美股和基金的证据驱动复盘 CLI，可生成 Markdown 报告和 JSON Evidence Packs，便于 AI Agent 审计与复用。

## 数据库

* [manahl/arctic: High performance datastore for time series and tick data](https://github.com/manahl/arctic) - 基于mongodb和python的高性能时间序列和tick数据存储
* [kdb | The Leader in High-Performance Tick Database Technology | Kx Systems](https://kx.com/) - 收费的高性能金融序列数据库解决方案
* [MongoDB Blog](http://blog.mongodb.org/post/65517193370/schema-design-for-time-series-data-in-mongodb) - 用mongodb存储时间序列数据
*  [InfluxDB – Time-Series Data Storage | InfluxData](https://www.influxdata.com/time-series-platform/influxdb/) - Go写的分布式时间序列数据库
* [OpenTSDB/opentsdb: A scalable, distributed Time Series Database.](https://github.com/OpenTSDB/opentsdb) - 基于HBase的时间序列数据库
* [kairosdb/kairosdb: Fast scalable time series database](https://github.com/kairosdb/kairosdb) -  基于Cassandra的时间序列数据库
* [timescale/timescaledb: An open-source time-series database optimized for fast ingest and complex queries. Engineered up from PostgreSQL, packaged as an extension.](https://github.com/timescale/timescaledb) -  基于PostgreSQL的时间序列数据库

## 量化交易平台

* [JoinQuant聚宽量化交易平台](https://www.joinquant.com/) - 一个基于Python的在线量化交易平台
* [优矿 - 通联量化实验室](https://uqer.io/home/) - 一个基于Python的在线量化交易平台
* [Ricequant 量化交易平台](https://www.ricequant.com/) - 支持Python和Java的在线量化交易平台
* [掘金量化](http://www.myquant.cn/) - 支持C/C++、C#、MATLAB、Python和R的量化交易平台
* [Auto-Trader](http://www.atrader.com.cn/portal.php) - 基于MATLAB的量化交易平台
* [MultiCharts 中国版 - 程序化交易软件](https://www.multicharts.cn/)
* [BotVS - 首家支持传统期货与股票证券与数字货币的量化平台](https://www.botvs.com/)
* [Tradeblazer(TB) - 交易开拓者](http://www.tradeblazer.net/) - 期货程序化交易软件平台
* [MetaTrader 5](https://www.metatrader5.com/en) - Multi-Asset Trading Platform
* [BigQuant](https://bigquant.com) - 专注量化投资的人工智能/机器学习平台
* [天勤量化（TqSdk）](https://github.com/shinnytech/tqsdk-python) - 快期出品的 Python 量化开发包，免费提供期货、期权、股票数据，支持实盘交易/历史回测
* [果仁网](https://guorn.com/) - 一个以选股+量化为主要特色的平台，不需要写代码就能完成大部分的量化和回测操作
* [godzilla.dev](https://godzilla.dev/) - 一个开源的 C++/Python 量化交易基础设施，用于自托管的加密货币资金费率套利与做市，具备超低延迟架构，并支持企业级私有化部署

## 策略
* [JoinQuant聚宽: 量化学习资料、经典交易策略、Python入门 - 雪球](https://xueqiu.com/8287840120/65009358)
* [myquant/strategy: 掘金策略集锦](https://github.com/myquant/strategy)
* [优矿社区内容索引](https://uqer.io/community/share/58243e7d228e5b91df6d5d19)
* [RiceQuant米筐量化社区 2016年4月以来优秀策略与研究汇总](https://www.ricequant.com/community/topic/1863//3)
* [雪球选股](https://xueqiu.com/9796081404)
* [botvs/strategies: 用Javascript OR Python进行量化交易](https://github.com/botvs/strategies)

## 回测
* [Zipline](https://github.com/quantopian/zipline) - 一个Python的回测框架
* [pyalgotrade](https://github.com/gbeced/pyalgotrade) - 一个Python的事件驱动回测框架
* [pyalgotrade-cn](https://github.com/Yam-cn/pyalgotrade-cn) - Pyalgotrade-cn在原版pyalgotrade的基础上加入了A股历史行情回测，并整合了tushare提供实时行情。
* [ricequant/rqalpha](https://github.com/ricequant/rqalpha) - RQalpha: Ricequant 开源的基于Python的回测引擎
* [quantdigger](https://github.com/QuantFans/quantdigger) - 基于python的量化回测框架,借鉴了主流商业软件（比如TB, 金字塔）简洁的策略语法
* [pyktrader](https://github.com/harveywwu/pyktrader) - 基于pyctp接口，并采用vnpy的eventEngine，使用tkinter作为GUI的python交易平台
* [QuantConnect/Lean](https://github.com/QuantConnect/Lean) -  Lean Algorithmic Trading Engine by QuantConnect (C#, Python, F#, VB, Java)
* [QUANTAXIS](https://github.com/yutiansut/QUANTAXIS) - QUANTAXIS 量化金融策略框架 - 中小型策略团队解决方案
* [Hikyuu](http://hikyuu.org) - 基于Python/C++的开源量化交易研究框架
* [StarQuant](https://github.com/physercoe/starquant) - 基于Python/C++的综合量化交易回测系统/平台
* [finclaw](https://github.com/NeuZhou/finclaw) - AI驱动的量化交易引擎，484个内置alpha因子，遗传算法策略进化，walk-forward回测和模拟交易

## 交易API
* [上海期货信息技术有限公司CTP API](http://www.sfit.com.cn/5_2_DocumentDown.htm) - 期货交易所提供的API
* [飞马快速交易平台 - 上海金融期货信息技术有限公司](http://www.cffexit.com.cn/static/3000201.html) - 飞马
* [大连飞创信息技术有限公司](http://www.dfitc.com.cn/portal/cate?cid=1364967839100#1) - 飞创
* [vnpy](https://github.com/vnpy/vnpy) - 基于python的开源交易平台开发框架
* [QuantBox/XAPI2](https://github.com/QuantBox/XAPI2) - 统一行情交易接口第2版
* [easytrader](https://github.com/shidenggui/easytrader) - 提供券商华泰/佣金宝/银河/广发/雪球的基金、股票自动程序化交易，量化交易组件
* [策略易](http://www.iguuu.com/e)（[SDK](https://github.com/sinall/StrategyEase-Python-SDK)）  - 管理交易客户端，提供基于 HTTP 协议的 RESTFul API；各大在线量化交易平台策略自动化解决方案
* [IB API | Interactive Brokers](https://www.interactivebrokers.com.hk/cn/index.php?f=5234&ns=T) - 盈透证券的交易API
* [FutunnOpen/futuquant](https://github.com/FutunnOpen/futuquant) - 富途量化平台 API


## 编程

### Python
#### 安装
* [Anaconda](https://www.continuum.io/downloads) - 推荐通过[清华大学镜像 ](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)下载安装
* [Python Extension Packages for Windows - Christoph Gohlke](http://www.lfd.uci.edu/~gohlke/pythonlibs/) - Windows用户从这里可以下载许多python库的预编译包

#### 教程
* [Python | Codecademy](https://www.codecademy.com/learn/python)
* [用 Python 玩转数据 - 南京大学 | Coursera](https://www.coursera.org/learn/hipython)
* [Introduction to Data Science in Python - University of Michigan | Coursera](https://www.coursera.org/learn/python-data-analysis)
* [The Python Tutorial — Python 3.5.2 documentation](https://docs.python.org/3/tutorial/)
* [Python for Finance](https://book.douban.com/subject/25921015/)
* [Algorithmic Thinking](https://www.coursera.org/learn/algorithmic-thinking-1) - Python 算法思维训练

#### 库
* [awesome-python: A curated list of awesome Python frameworks, libraries, software and resources](https://github.com/vinta/awesome-python)
* [pandas](http://pandas.pydata.org) - Python做数据分析的基础
* [pyql: Cython QuantLib wrappers](https://github.com/enthought/pyql)
* [ffn](http://pmorissette.github.io/ffn/quick.html) - 绩效评估
* [ta-lib: Python wrapper for TA-Lib (http://ta-lib.org/).](https://github.com/mrjbq7/ta-lib) - 技术指标
* [StatsModels: Statistics in Python — statsmodels documentation](http://statsmodels.sourceforge.net/) - 常用统计模型
* [arch: ARCH models in Python](https://github.com/bashtage/arch) - 时间序列
* [pyfolio: Portfolio and risk analytics in Python](https://github.com/quantopian/pyfolio) - 组合风险评估
* [twosigma/flint: A Time Series Library for Apache Spark](https://github.com/twosigma/flint) - Apache Spark上的时间序列库
* [PyFlux](https://github.com/RJT1990/pyflux) - Python 的时间序列建模(频率派和贝叶斯)  

### R

#### 安装
* [The Comprehensive R Archive Network](https://mirrors.tuna.tsinghua.edu.cn/CRAN/) - 从国内清华镜像下载安装
* [RStudio](https://www.rstudio.com/products/rstudio/download/) - R的常用开发平台下载

#### 教程
* [Free Introduction to R Programming Online Course](https://www.datacamp.com/courses/free-introduction-to-r) - datacamp的在线学习
* [R Programming - 约翰霍普金斯大学 | Coursera](https://www.coursera.org/learn/r-programming)
* [Intro to Computational Finance with R](https://www.datacamp.com/community/open-courses/computational-finance-and-financial-econometrics-with-r) - 用R进行计算金融分析

#### 库
* [CRAN Task View: Empirical Finance](https://cran.r-project.org/web/views/Finance.html) - CRAN官方的R金融相关包整理
* [qinwf/awesome-R: A curated list of awesome R packages, frameworks and software.](https://github.com/qinwf/awesome-R) - R包的awesome

### C++
#### 教程
* [C++程序设计](http://www.xuetangx.com/courses/course-v1:PekingX+04831750.1x+2015T1/about) - 北京大学  郭炜
* [基于Linux的C++ ](http://www.xuetangx.com/courses/course-v1:TsinghuaX+20740084X+sp/about) - 清华大学  乔林
* [面向对象程序设计（C++）](http://www.xuetangx.com/courses/course-v1:TsinghuaX+30240532X+sp/about) - 清华大学 徐明星
*  [C++ Design Patterns and Derivatives Pricing ](https://book.douban.com/subject/1485468/) - C++设计模式
* [C++ reference - cppreference.com](http://en.cppreference.com/w/cpp) - 在线文档

#### 库
* [fffaraz/awesome-cpp: A curated list of awesome C/C++ frameworks, libraries, resources, and shiny things.](https://github.com/fffaraz/awesome-cpp) - C++库整理
* [rigtorp/awesome-modern-cpp: A collection of resources on modern C++](https://github.com/rigtorp/awesome-modern-cpp) - 现代C++库整理
* [QuantLib: a free/open-source library for quantitative finance](http://quantlib.org/index.shtml)
* [libtrading/libtrading: Libtrading, an ultra low-latency trading connectivity library for C and C++.](https://github.com/libtrading/libtrading)
* [NexusFix](https://github.com/SilverstreamsAI/NexusFix) - C++23 高性能 FIX 协议引擎，零拷贝解析 + SIMD 加速，解析 ExecutionReport ~246ns（QuickFIX ~730ns）

### Julia
#### 教程
* [Learning Julia](http://julialang.org/learning/) - 官方整理
* [QUANTITATIVE ECONOMICS with Julia](http://quant-econ.net/_static/pdfs/jl-quant-econ.pdf) - 经济学诺奖获得者Thomas Sargent教你[Julia](http://julialang.org/)在量化经济的应用。

#### 库
* [Quantitative Finance in Julia](https://github.com/JuliaQuant) - 多数为正在实现中，感兴趣的可以参与

### 编程论坛
- [Stack Overflow](http://stackoverflow.com/) - 对应语言的tag
- [SegmentFault](https://segmentfault.com/) - 对应语言的tag

### 编程能力在线训练

* [Solve Programming Questions | HackerRank](https://www.hackerrank.com/domains) - 包含常用语言(C++, Java, Python, Ruby, SQL)和相关计算机应用技术(算法、数据结构、数学、AI、Linux Shell、分布式系统、正则表达式、安全)的教程和挑战。
* [LeetCode Online Judge](https://leetcode.com/) - C, C++, Java, Python, C#, JavaScript, Ruby, Bash, MySQL在线编程训练

## 论坛
* [Quantitative Finance StackExchange](http://quant.stackexchange.com/) -  stackexchange 系列的 quant 论坛
* [JoinQuant社区](https://www.joinquant.com/community) - JoinQuant社区
* [优矿社区](https://uqer.io/community/list) - 优矿社区
* [RiceQuant量化社区](https://www.ricequant.com/community/) - RiceQuant量化社区
* [掘金量化社区](http://forum.myquant.cn/) - 掘金量化社区
* [清华大学学生经济金融论坛](http://forum.thuquant.com/) - 清华大学学生金融数据与量化投资协会主办

## 书籍
* [My Life as a Quant: Reflections on Physics and Finance](http://www.amazon.com/My-Life-Quant-Reflections-Physics/dp/0470192739) - In My Life as a Quant, Emanuel Derman relives his exciting journey as one of the first high-energy particle physicists to migrate to Wall Street.
* [量化交易](https://book.douban.com/subject/25878150/) - Ernest P. Chan撰写的量化投资理论
* [量化投资与对冲基金丛书：波动率交易](https://book.douban.com/subject/25711100/)
* [Following the Trend](https://book.douban.com/subject/19990593/)
* [Statistical Inference](https://book.douban.com/subject/1464795/) - 统计推断入门
* [All of Nonparametric Statistics](https://book.douban.com/subject/4251603/) - 非参统计入门
* [The Elements of Statistical Learning](https://book.douban.com/subject/3294335/) -  Data Mining, Inference, and Prediction
* [Analysis of Financial Time Series](https://book.douban.com/subject/4719140/) - Ruey S. Tsay  的时间序列分析
* [Options, Futures, and Other Derivatives](https://book.douban.com/subject/6127888/) - 期权期货等衍生品



## 论文
* [awesome-quant/papers.md](https://github.com/thuquant/awesome-quant/blob/master/papers.md)

## 值得关注的信息源
* [Quantitative Finance arxiv](https://arxiv.org/archive/q-fin)
* [雪球工程师1号](http://xueqiu.com/engineer) - 财经社交网络雪球的量化相关账号。
* [Ricequant量化](http://xueqiu.com/ricequant) - Ricequant量化平台的雪球账号。
* [量化哥-优矿Uqer](http://xueqiu.com/4105947155) - 优矿Uqer量化平台的雪球账号。
* [宽客 (Quant) - 索引 - 知乎](https://www.zhihu.com/topic/19557481)
* 量化投资与机器学习 - 微信公众号
* THU量协 - 微信公众号
* 优矿量化实验室  - 微信公众号
* Ricequant   - 微信公众号
* 鲁明量化全视角 - 微信公众号


## 政策
* [中国证券监督管理委员会](http://www.csrc.gov.cn/pub/newsite/)
* [考试报名-中国证券业协会](http://www.sac.net.cn/cyry/kspt/ksbm/) - 证券从业资格报名
* [中国证券投资基金业协会](http://www.amac.org.cn/) - 内有相关法规教育和从业资格报名入口
* [大连商品交易所](http://www.dce.com.cn/)
* [上海期货交易所首页](http://www.shfe.com.cn/)
* [郑州商品交易所网站](http://www.czce.com.cn/portal/index.htm)
* [上海证券交易所](http://www.sse.com.cn/)
* [深圳证券交易所](http://www.szse.cn/)

# 其他Quant资源索引

* [Quantitative Finance Reading List - QuantStart](https://www.quantstart.com/articles/Quantitative-Finance-Reading-List#general-quant-finance-reading)
* [Master reading list for Quants, MFE (Financial Engineering) students | QuantNet Community](https://www.quantnet.com/threads/master-reading-list-for-quants-mfe-financial-engineering-students.535/)

# 其他 Awesome 列表
* 英文版 awesome-quant [wilsonfreitas/awesome-quant: A curated list of insanely awesome libraries, packages and resources for Quants (Quantitative Finance)](https://github.com/wilsonfreitas/awesome-quant)
* Other awesome lists [awesome-awesomeness](https://github.com/bayandin/awesome-awesomeness).
* Even more lists [awesome](https://github.com/sindresorhus/awesome).
* Another list? [list](https://github.com/jnv/lists).
* WTF! [awesome-awesome-awesome](https://github.com/t3chnoboy/awesome-awesome-awesome).
* Analytics [awesome-analytics](https://github.com/onurakpolat/awesome-analytics).
