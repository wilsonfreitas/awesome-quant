
import requests
import re
import pandas as pd

reu = re.compile('https://github.com/([\w-]+/[\w-]+)')

url = 'https://cran.r-project.org/web/packages/xts/index.html'

urls = [
    'https://cran.r-project.org/web/packages/xts/index.html',
    'https://cran.r-project.org/web/packages/data.table/index.html',
    'https://cran.r-project.org/web/packages/tseries/index.html',
    'https://cran.r-project.org/web/packages/zoo/index.html',
    'https://cran.r-project.org/web/packages/tis/index.html',
    'https://cran.r-project.org/web/packages/tfplot/index.html',
    'https://cran.r-project.org/web/packages/tframe/index.html',
    'https://cran.r-project.org/web/packages/IBrokers/index.html',
    'https://cran.r-project.org/web/packages/Rblpapi/index.html',
    'https://cran.r-project.org/web/packages/Rbitcoin/index.html',
    'https://cran.r-project.org/web/packages/GetTDData/index.html',
    'https://cran.r-project.org/web/packages/GetHFData/index.html',
    'https://cran.r-project.org/package=td',
    'https://cran.r-project.org/web/packages/quantmod/index.html',
    'https://cran.r-project.org/web/packages/fAsianOptions/index.html',
    'https://cran.r-project.org/web/packages/fAssets/index.html',
    'https://cran.r-project.org/web/packages/fBasics/index.html',
    'https://cran.r-project.org/web/packages/fBonds/index.html',
    'https://cran.r-project.org/web/packages/fExoticOptions/index.html',
    'https://cran.r-project.org/web/packages/fOptions/index.html',
    'https://cran.r-project.org/web/packages/fPortfolio/index.html',
    'https://cran.r-project.org/web/packages/portfolio/index.html',
    'https://cran.r-project.org/web/packages/portfolioSim/index.html',
    'https://cran.r-project.org/web/packages/sde/index.html',
    'https://cran.r-project.org/web/packages/YieldCurve/index.html',
    'https://cran.r-project.org/web/packages/SmithWilsonYieldCurve/index.html',
    'https://cran.r-project.org/web/packages/ycinterextra/index.html',
    'https://cran.r-project.org/web/packages/AmericanCallOpt/index.html',
    'https://cran.r-project.org/web/packages/VarSwapPrice/index.html',
    'https://cran.r-project.org/web/packages/RND/index.html',
    'https://cran.r-project.org/web/packages/LSMonteCarlo/index.html',
    'https://cran.r-project.org/web/packages/OptHedging/index.html',
    'https://cran.r-project.org/web/packages/tvm/index.html',
    'https://cran.r-project.org/web/packages/OptionPricing/index.html',
    'https://cran.r-project.org/web/packages/credule/index.html',
    'https://cran.r-project.org/web/packages/derivmkts/index.html',
    'https://cran.r-project.org/web/packages/PortfolioAnalytics/PortfolioAnalytics.pdf',
    'https://cran.r-project.org/web/packages/backtest/index.html',
    'https://cran.r-project.org/web/packages/pa/index.html',
    'https://cran.r-project.org/web/packages/TTR/index.html',
    'https://cran.r-project.org/web/packages/PerformanceAnalytics/index.html',
    'https://cran.r-project.org/web/packages/tseries/index.html',
    'https://cran.r-project.org/web/packages/zoo/index.html',
    'https://cran.r-project.org/web/packages/xts/index.html',
    'https://cran.r-project.org/web/packages/fGarch/index.html',
    'https://cran.r-project.org/web/packages/timeSeries/index.html',
    'https://cran.r-project.org/web/packages/rugarch/index.html',
    'https://cran.r-project.org/web/packages/rmgarch/index.html',
    'https://cran.r-project.org/web/packages/timeDate/index.html',
    'https://cran.r-project.org/web/packages/bizdays/index.html',
]


def get_data(url):
    res = requests.get(url)
    m = reu.search(res.text)
    if m:
        return dict(cran=url, github=m.group(0), repo=m.group(1))
    else:
        return dict(cran=url, github='', repo='')


all_data = [get_data(url) for url in urls]
df = pd.DataFrame(all_data)
df.to_csv('cran.csv', index=False)
