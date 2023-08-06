# StockHero

[![Downloads](https://pepy.tech/badge/stockhero)](https://pepy.tech/project/stockhero)

## New Features in 0.2.3
* Yahoo Finance is partly supported
* fixed some bugs
* MultiIndex looks pretty useful

### New Features planned for the next release
- [ ] clean up the code
- [ ] combine some functions
- [ ] np.NaN for any not valid value
- [ ] give back None for any empty pd.dataframe

## The Ticker module
The ```Ticker``` module, gets the financial data from nasdaq.com, morningstar.com, yahoo.com as a pandas.DataFrame <br>

```python
import StockHero as stock
nvda = stock.Ticker('NVDA') # e.g. NVIDIA Corp

nvda.financials                         # Morningstar - Financials
nvda.marginofsales                      # Morningstar - Margins % of Sales
nvda.profitability                      # Morningstar - Profitability
nvda.growth_rev                         # Morningstar - Growth - Revenue %
nvda.growth_op_inc                      # Morningstar - Growth - Operating Income %
nvda.growth_net_inc                     # Morningstar - Growth - Net Income %
nvda.growth_eps                         # Morningstar - Growth - EPS %
nvda.cf_ratios                          # Morningstar - Cash Flow - Cash Flow Ratios
nvda.bs                                 # Morningstar - Balance Sheet Items (in %)
nvda.li_fin                             # Morningstar - Liquidity/Financial Health
nvda.efficiency                         # Morningstar - Efficiency
nvda.morningstar_quote                  # Morningstar - Quote

nvda.yahoo_statistics                   # Yahoo Finance - Statistics

nvda.nasdaq_summ                        # Nasdaq      - Summary
nvda.nasdaq_div_hist                    # Nasdaq      - Dividend History
nvda.nasdaq_hist_quotes_stock           # Nasdaq      - Historical Quotes for Stocks
nvda.nasdaq_hist_quotes_etf             # Nasdaq      - Historical Quotes for ETFs
nvda.nasdaq_hist_nocp                   # Nasdaq      - Historical Nasdaq Official Closing Price (NOCP)
nvda.nasdaq_fin_income_statement_y      # Nasdaq      - Financials - Income Statement - Yearly
nvda.nasdaq_fin_balance_sheet_y         # Nasdaq      - Financials - Balance Sheet    - Yearly
nvda.nasdaq_fin_cash_flow_y             # Nasdaq      - Financials - Cash Flow        - Yearly
nvda.nasdaq_fin_fin_ratios_y            # Nasdaq      - Financials - Financial Ratios - Yearly
nvda.nasdaq_fin_income_statement_q      # Nasdaq      - Financials - Income Statement - Quarterly
nvda.nasdaq_fin_balance_sheet_q         # Nasdaq      - Financials - Balance Sheet    - Quarterly
nvda.nasdaq_fin_cash_flow_q             # Nasdaq      - Financials - Cash Flow        - Quarterly
nvda.nasdaq_fin_fin_ratios_q            # Nasdaq      - Financials - Financial Ratios - Quarterly
nvda.nasdaq_earn_date_eps               # Nasdaq      - Earnings Date - Earnings Per Share
nvda.nasdaq_earn_date_surprise          # Nasdaq      - Earnings Date - Quarterly Earnings Surprise Amount
nvda.nasdaq_yearly_earn_forecast        # Nasdaq      - Earnings Date - Yearly Earnings Forecast 
nvda.nasdaq_quarterly_earn_forecast     # Nasdaq      - Earnings Date - Quarterly Earnings Forecast 
nvda.nasdaq_pe_forecast                 # Nasdaq      - Price/Earnings & PEG Ratios - Price/Earnings Ratio
nvda.nasdaq_gr_forecast                 # Nasdaq      - Price/Earnings & PEG Ratios - Forecast P/E Growth Rates
nvda.nasdaq_peg_forecast                # Nasdaq      - Price/Earnings & PEG Ratios - PEG Ratio
```

## The StockExchange module
The ```StockExchange``` module, gets the financial data from the Nasdaq Stock Screener as a pandas.DataFrame <br>
Currently only the Nasdaq is supported, the plan is to support more markets (time will tell)

```python
import StockHero as stock
t = stock.StockExchange('something') # e.g. Nasdaq

t.nasdaq                # Nasdaq Stock Market

```

## Combining both modules
You can combine both modules, for example
```python
import StockHero as stock
t = stock.StockExchange('something')

df = t.nasdaq
ticker = df.loc[df['Name'].str.contains('NVIDIA'), 'Symbol'].values[0]
n = stock.Ticker(ticker)
n.financials
```


### Installing
https://pypi.org/project/StockHero/

### Legal Stuff

StockHero is distributed under the Apache Software License

### Any feedback or suggestions, let me know
Or in the words of Peter Thiel:
> We wanted flying cars, instead we got 140 characters

<br>
<br>
### Versions <br>
0.2.3 Bug fixes and added first data from Yahoo Finance <br>
0.2.2 Bug fixes and added more data from Morningstar <br>
0.2.1 Added more data from nasdaq.com <br>
0.1.1 Bug fixes <br>
0.1.0 Added the StockExchange modul <br>
0.0.2 Bug fixes / Changed License <br>
0.0.1 First Release

