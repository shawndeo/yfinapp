import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title('Dividend Aristocrats')
#
st.sidebar.title('Configurations')

option = st.sidebar.selectbox('Pick a Dividend Aristocrat:',
('ABBV', 'ABT', 'ADP', 'AFL', 'ALB',
'AMCR', 'AOS', 'APD', 'ATO', 'BDX',
'BEN', 'BF-B', 'CAH', 'CAT', 'CB',
'CINF', 'CL', 'CLX', 'CTAS', 'CVX',
'DOV', 'ECL', 'ED', 'EMR', 'ESS',
'EXPD', 'FRT', 'GD', 'GPC', 'GWW',
'HRL', 'IBM', 'ITW', 'JNJ', 'KMB',
'KO', 'LEG', 'LIN', 'LOW', 'MCD',
'MDT', 'MKC', 'MMM', 'MSFT', 'NEE',
'NUE', 'O', 'PBCT', 'PEP', 'PG',
'PNR', 'PPG', 'ROP', 'SHW', 'SPGI',
'SWK', 'SYY', 'T', 'TGT', 'TROW',
'VFC', 'WBA', 'WMT', 'WST', 'XOM'))

SP500 = yf.Ticker('^GSPC')

st.header(f"{option}'s 1-Year Performance vs S&P 500's 1-Year Performance")

SP500pct = pd.DataFrame(SP500.history(period = '1y',
                                        interval = '1d').Close)

SP500pct = SP500pct / SP500pct.iloc[0]

pick = yf.Ticker(option)

optvs500 = SP500pct

optvs500[f'{option}'] = pick.history(period = '1y',
                                    interval = '1d').Close / pick.history(period = '1y',
                                                                            interval = '1d').Close[0]

st.line_chart(optvs500)

st.write(optvs500)

st.header(f'{option} Dividend Growth History')

divPayoutHist = pick.history(period = 'max')
divPayoutHist = pick.dividends

#st.write(divPayoutHist[-1], divPayoutHist[0])

st.line_chart(divPayoutHist)

st.write(divPayoutHist)

st.sidebar.header('S&P 500 1-Year Performance')

SP5001YearPerf = round(((SP500pct['Close'][-1] - 1) * 100), 2)
st.sidebar.write(f'{SP5001YearPerf}%')

pick1YearPerf = round(((optvs500[option][-1] - 1) * 100), 2)

st.sidebar.header(f"{option}'s 1-Year Performance")
st.sidebar.write(f'{pick1YearPerf}%')

st.sidebar.header('Outperforms/Underperforms by:')
st.sidebar.write(f'{round((pick1YearPerf - SP5001YearPerf), 2)}%')

pickDividendGrowth = (divPayoutHist[-1] / divPayoutHist[0]) - 1
pickDividendTimeFrame = round(((divPayoutHist.index[-1] - divPayoutHist.index[0]).days) / 365)

st.sidebar.header("Approximate Annual Dividend Growth:")
st.sidebar.write(f'{round((pickDividendGrowth / pickDividendTimeFrame) * 100, 2)}%')

st.sidebar.header('1-Year Dividend Growth:')

divPayoutHist = pick.history(period = '1y')
st.sidebar.write(f"{round(((pick.dividends[-1] / pick.dividends[0]) - 1) * 100, 2)}%")
