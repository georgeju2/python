# version 1.2
# Add new 2024/12
#
import yfinance as yf
import pandas as pd
import datetime
from datetime import timedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

last_dt_prev_year = datetime.date(2023, 12, 29)

tickers=['VTCLX', 'VBTLX', 'VTMSX', 'VIPSX', 'VFIAX', 'VTIAX', 'VMRXX', 'VTMGX', 'VMSXX', 'VEMAX']
print(tickers)

downloaded = yf.download(tickers = tickers, period='1y', interval='1d')
histpx=downloaded['Adj Close'].sort_index(ascending=False)
histpx.index=histpx.index.date

tk_2_name_d = {}


def get_return(px, d1, d2):
    print(px[d2] - px[d1])


for tk in tickers:
    gfi = yf.Ticker(tk)
    tk_2_name_d[tk] = gfi.info['shortName']
    print(tk, gfi.info['shortName'])

def last_friday():
    return datetime.date(2024, 1, 19)

def one_week_before(d1):
    return d1 - datetime.timedelta(days=7)

def pick_weekly_data(data, k=4):
    assert k <= 6 and k >= 0
    return data[list(map(lambda d: datetime.date.weekday(d) == k, data.index.tolist()))]

def get_name(r):
    #print(r.name)
    fund_name = tk_2_name_d[r.name].replace("Vanguard ", "")
    return fund_name

if __name__=="__main__":
    for tk in tickers:
        last_yr_close = histpx.loc[last_dt_prev_year][tk]
        last= last_friday()
        one_wk_before = one_week_before(last)
        last_px = histpx.loc[last][tk]
        prev_weekly_px =histpx.loc[one_wk_before][tk]
        onewk_earlier = one_week_before(last)
        wk_ret = round((last_px-prev_weekly_px)/prev_weekly_px*100, 2)
        ytd_ret = round((last_px-last_yr_close)/last_yr_close*100, 2)
        print(f"{wk_ret} (%),  {ytd_ret} ", tk, tk_2_name_d[tk])

    price_dates = [last_dt_prev_year, one_wk_before, last]
    prices = histpx.loc[price_dates].T
    prices.loc[:, 'fund name'] = prices.apply(get_name, axis=1)
    prices.loc[:, '1_wk (%)'] = round( (prices[last] - prices[one_wk_before])/prices[one_wk_before]*100,2)
    prices.loc[:, 'ytd (%)'] = round((prices[last] - prices[last_dt_prev_year])/prices[last_dt_prev_year]*100, 2)
    for px_dt in price_dates:
        prices.loc[:, px_dt] = round(prices[px_dt], 3)
    prices = prices.sort_values('ytd (%)')

    print(prices)
