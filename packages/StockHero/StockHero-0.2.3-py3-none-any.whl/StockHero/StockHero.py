# -*- coding: utf-8 -*-
"""
Created on Wed Oct  20 17:51:58 2021

@author: RobWen
Version: 0.2.3
"""
import pandas as pd
import requests
from pandas import json_normalize
from bs4 import BeautifulSoup
import numpy as np

class Ticker:
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = self.__get_data()
        self.__laenge()
        self.headers_standard = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}
    
    def __repr__(self):
        return(self.ticker)
        
    def __str__(self):
        return(self.ticker)
       
    @property
    def financials(self):
        return self.__morningstar_financials()
    
    @property
    def marginofsales(self):
        return self.__morningstar_margins_of_sales()
    
    @property
    def profitability(self):
        return self.__morningstar_profitability()
    
    @property
    def growth_rev(self):
        return self.__morningstar_growth_revenue()
    
    @property
    def growth_op_inc(self):
        return self.__morningstar_growth_operating_income()
    
    @property
    def growth_net_inc(self):
        return self.__morningstar_growth_net_income()
    
    @property
    def growth_eps(self):
        return self.__morningstar_growth_eps()
    
    @property
    def cf_ratios(self):
        return self.__morningstar_cashflow_ratios()
    
    @property
    def bs(self):
        return self.__morningstar_finhealth_bs()
    
    @property
    def li_fin(self):
        return self.__morningstar_finhealth_health()
    
    @property
    def efficiency(self):
        return self.__morningstar_effiency_ratios()
    
    @property
    def morningstar_quote(self):
        return self.__morningstar_quote_df()
    
    @property
    def nasdaq_summ(self):
        return self.__nasdaq_summary_df()
    
    @property
    def nasdaq_div_hist(self):
        return self.__nasdaq_dividend_history_df()
    
    @property
    def nasdaq_hist_quotes_stock(self):
        return self.__nasdaq_historical_data_stock_df()
    
    @property
    def nasdaq_hist_quotes_etf(self):
        return self.__nasdaq_historical_data_etf_df()
    
    @property
    def nasdaq_hist_nocp(self):
        return self.__nasdaq_historical_nocp_df()
    
    @property
    def nasdaq_fin_income_statement_y(self):
        return self.__nasdaq_financials_income_statement_y_df()
    
    @property
    def nasdaq_fin_balance_sheet_y(self):
        return self.__nasdaq_financials_balance_sheet_y_df()
    
    @property
    def nasdaq_fin_cash_flow_y(self):
        return self.__nasdaq_financials_cash_flow_y_df()
    
    @property
    def nasdaq_fin_fin_ratios_y(self):
        return self.__nasdaq_financials_financials_ratios_y_df()
    
    @property
    def nasdaq_fin_income_statement_q(self):
        return self.__nasdaq_financials_income_statement_q_df()
    
    @property
    def nasdaq_fin_balance_sheet_q(self):
        return self.__nasdaq_financials_balance_sheet_q_df()
    
    @property
    def nasdaq_fin_cash_flow_q(self):
        return self.__nasdaq_financials_cash_flow_q_df()
    
    @property
    def nasdaq_fin_fin_ratios_q(self):
        return self.__nasdaq_financials_financials_ratios_q_df()
    
    @property
    def nasdaq_earn_date_eps(self):
        return self.__nasdaq_earnings_date_eps_df()
    
    @property
    def nasdaq_earn_date_surprise(self):
        return self.__nasdaq_earnings_date_surprise_df()
    
    @property
    def nasdaq_yearly_earn_forecast(self):
        return self.__nasdaq_earnings_date_yearly_earnings_forecast_df()
    
    @property
    def nasdaq_quarterly_earn_forecast(self):
        return self.__nasdaq_earnings_date_quarterly_earnings_forecast_df()
    
    @property
    def nasdaq_pe_forecast(self):
        return self.__forecast_pe_df()
    
    @property
    def nasdaq_gr_forecast(self):
        return self.__forecast_gr_df()
    
    @property
    def nasdaq_peg_forecast(self):
        return self.__forecast_peg_df()
    
    @property
    def yahoo_statistics(self):
        return self.__yahoo_statistics_df()
    
    def __get_data(self):
        
        headers = {'Referer': f'http://financials.morningstar.com/ratios/r.html?t={self.ticker}'}
        r = requests.get(f"http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&t={self.ticker}", headers=headers)
        csvdatei = r.content
        
        my_decoded_str = csvdatei.decode()
        my_decoded_str = my_decoded_str.split()
        
        return my_decoded_str
    
    def __laenge(self):
        if len(self.data) == 304:
            self.length = 0
        elif len(self.data) == 305:
            self.length = 1
        elif len(self.data) == 306:
            self.length = 2
        elif len(self.data) == 307:
            self.length = 3
        elif len(self.data) == 308:
            self.length = 4
        else:
            self.length = 5
    
    # e.g. https://www.morningstar.com/stocks/xnas/nvda/quote
    def __morningstar_quote_df(self):
        
        url = f'https://www.morningstar.com/stocks/xnas/{self.ticker}/quote'
        
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        text = page.find_all(text=True)
        
        string = text[-4].replace('"','').strip().split(',')
        
        for n,i in enumerate(string):
            if string[n] == 'Qual' or string[n] == 'Quant':
                parameter = n
                break
            
        morningstar_performance_id = string[parameter+1]
        
        url = f'https://api-global.morningstar.com/sal-service/v1/stock/header/v2/data/{morningstar_performance_id}/securityInfo?showStarRating=&languageId=en&locale=en&clientId=MDC&benchmarkId=category&component=sal-components-quote&version=3.49.0'
        
        headers = {
            'ApiKey': 'lstzFDEOhfFNMLikKa0am9mgEKLBl49T',
        }
        
        r = requests.get(url, headers=headers)
        dictionary = r.json()
        
        priceEarnings = dictionary["priceEarnings"]
        priceBook = dictionary["priceBook"]
        priceSale = dictionary["priceSale"]
        forwardPE = dictionary["forwardPE"]
        forwardDivYield = dictionary["forwardDivYield"]
        
        url = f'https://api-global.morningstar.com/sal-service/v1/stock/keyStats/{morningstar_performance_id}?languageId=en&locale=en&clientId=MDC&benchmarkId=category&component=sal-components-quote&version=3.49.0'
        
        headers = {
            'ApiKey': 'lstzFDEOhfFNMLikKa0am9mgEKLBl49T',
        }
        
        r = requests.get(url, headers=headers)
        json = r.json()
        
        revenue3YearGrowth = json['revenue3YearGrowth']['stockValue']
        netIncome3YearGrowth = json['netIncome3YearGrowth']['stockValue']
        operatingMarginTTM = json['operatingMarginTTM']['stockValue']
        netMarginTTM = json['netMarginTTM']['stockValue']
        roaTTM = json['roaTTM']['stockValue']
        roeTTM = json['roeTTM']['stockValue']
        freeCashFlowTTM = json['freeCashFlow']['cashFlowTTM']
        
        try:
            priceEarnings = '{:.2f}'.format(float(priceEarnings))
            priceBook = '{:.2f}'.format(float(priceBook))
            priceSale = '{:.2f}'.format(float(priceSale))
            forwardPE = '{:.2f}'.format(float(forwardPE))
            forwardDivYield = float(forwardDivYield) * 100 # in %
            revenue3YearGrowth = '{:.2f}'.format(float(revenue3YearGrowth))
            netIncome3YearGrowth = '{:.2f}'.format(float(netIncome3YearGrowth))
            operatingMarginTTM = '{:.2f}'.format(float(operatingMarginTTM))
            netMarginTTM = '{:.2f}'.format(float(netMarginTTM))
            roaTTM = '{:.2f}'.format(float(roaTTM))
            roeTTM = '{:.2f}'.format(float(roeTTM))
            freeCashFlowTTM = '{:,.2f}'.format(float(freeCashFlowTTM)) # locale='en_US'
        except(TypeError):
            pass
        
        df_morningstar_quote = pd.DataFrame([priceEarnings, priceBook, priceSale, forwardPE, forwardDivYield
                           , revenue3YearGrowth, netIncome3YearGrowth, operatingMarginTTM, netMarginTTM, roaTTM, roeTTM
                           , freeCashFlowTTM]
                          , index =['Price/Earnings', 'Price/Book', 'Price/Sales', 'Consensus Forward P/E', 'Forward Div Yield %'
                                    , 'Rev 3-Yr Growth', 'Net Income 3-Yr Growth'
                                    , 'Operating Margin % TTM', 'Net Margin % TTM', 'ROA % TTM'
                                    , 'ROE % TTM', 'Current Free Cash Flow']
                          , columns =['Ratio'])
        
        return df_morningstar_quote
    
    def __morningstar_financials(self):
                
        data = self.data
        length = self.length
            
        df_morningstar_financials = pd.DataFrame([Ticker.__data_list(data[12+length]), Ticker.__data_list(data[15+length])
                                        , Ticker.__data_list(data[19+length]), Ticker.__data_list(data[22+length])
                                        , Ticker.__data_list(data[26+length]), Ticker.__data_list(data[30+length])
                                        , Ticker.__data_list(data[32+length]), Ticker.__data_list(data[36+length])
                                        , Ticker.__data_list(data[38+length]), Ticker.__data_list(data[44+length])
                                        , Ticker.__data_list(data[49+length]), Ticker.__data_list(data[53+length])
                                        , Ticker.__data_list(data[58+length]), Ticker.__data_list(data[65+length])
                                        , Ticker.__data_list(data[69+length])]
                      , index =[Ticker.__index(data[10+length] + ' ' + data[11+length] + ' ' + data[12+length])
                                , Ticker.__index(data[13+length] + ' ' + data[14+length] + ' ' + data[15+length])
                                , Ticker.__index(data[16+length] + ' ' + data[17+length] + ' ' + data[18+length]+ ' ' + data[19+length])
                                , Ticker.__index(data[20+length] + ' ' + data[21+length] + ' ' + data[22+length])
                                , Ticker.__index(data[23+length] + ' ' + data[24+length] + ' ' + data[25+length]+ ' ' + data[26+length])
                                , Ticker.__index(data[27+length] + ' ' + data[28+length] + ' ' + data[29+length]+ ' ' + data[30+length])
                                , Ticker.__index(data[31+length] + ' ' + data[32+length])
                                , Ticker.__index(data[33+length] + ' ' + data[34+length] + ' ' + data[35+length]+ ' ' + data[36+length])
                                , Ticker.__index(data[37+length] + ' ' + data[38+length])
                                , Ticker.__index(data[39+length] + ' ' + data[40+length] + ' ' + data[41+length]+ ' ' + data[42+length]+ ' ' + data[43+length]+ ' ' + data[44+length])
                                , Ticker.__index(data[45+length] + ' ' + data[46+length] + ' ' + data[47+length]+ ' ' + data[48+length]+ ' ' + data[49+length])
                                , Ticker.__index(data[50+length] + ' ' + data[51+length] + ' ' + data[52+length]+ ' ' + data[53+length])
                                , Ticker.__index(data[54+length] + ' ' + data[55+length] + ' ' + data[56+length]+ ' ' + data[57+length]+ ' ' + data[58+length])
                                , Ticker.__index(data[59+length] + ' ' + data[60+length] + ' ' + data[61+length]+ ' ' + data[62+length]+ ' ' + data[53+length]+ ' ' + data[64+length]+ ' ' + data[65+length])
                                , Ticker.__index(data[66+length] + ' ' + data[67+length] + ' ' + data[68+length]+ ' ' + data[69+length])]
                      , columns = Ticker.__data_list(data[8+length] + data[9+length]))
    
        return df_morningstar_financials
    
    def __morningstar_margins_of_sales(self):
        
        data = self.data
        length = self.length
        
        self.morningstar_margins_of_sales = pd.DataFrame([Ticker.__data_list(data[78+length]), Ticker.__data_list(data[79+length])
                                              , Ticker.__data_list(data[81+length]), Ticker.__data_list(data[82+length])
                                              , Ticker.__data_list(data[83+length]), Ticker.__data_list(data[84+length])
                                              , Ticker.__data_list(data[86+length]), Ticker.__data_list(data[91+length])
                                              , Ticker.__data_list(data[93+length])]
                          , index =['Revenue', 'COGS', 'Gross Margin', 'SG&A'
                                    , 'R&D', 'Other', 'Operating Margin', 'Net Int Inc & Other', 'EBT Margin']
                          , columns = Ticker.__data_list(data[77+length]))
        
        return self.morningstar_margins_of_sales
    
    def __morningstar_profitability(self):
        
        data = self.data
        length = self.length
    
        self.morningstar_profitability = pd.DataFrame([Ticker.__data_list(data[97+length]), Ticker.__data_list(data[100+length])
                                           , Ticker.__data_list(data[103+length]), Ticker.__data_list(data[107+length])
                                           , Ticker.__data_list(data[110+length]), Ticker.__data_list(data[114+length])
                                           , Ticker.__data_list(data[119+length]), Ticker.__data_list(data[121+length])]
                      , index =['Tax Rate %', 'Net Margin %', 'Asset Turnover (Average)', 'Return on Assets %'
                                , 'Financial Leverage (Average)', 'Return on Equity %', 'Return on Invested Capital %'
                                ,'Interest Coverage']
                      , columns = Ticker.__data_list(data[94+length]))
    
        return self.morningstar_profitability
    
    
    def __morningstar_growth_revenue(self):
        
        data = self.data
        length = self.length
        
        self.morningstar_growth_revenue = pd.DataFrame([Ticker.__data_list(data[132+length]), Ticker.__data_list(data[134+length])
                                            , Ticker.__data_list(data[136+length]), Ticker.__data_list(data[138+length])]
                      , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                      , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_revenue
    
    def __morningstar_growth_operating_income(self):
        
        data = self.data
        length = self.length
        
        self.morningstar_growth_operating_income = pd.DataFrame([Ticker.__data_list(data[144+length]), Ticker.__data_list(data[146+length])
                                                     , Ticker.__data_list(data[148+length]), Ticker.__data_list(data[150+length])]
                        , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                        , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_operating_income
    
    def __morningstar_growth_net_income(self):
        
        data = self.data
        length = self.length
        
        try: 
            self.morningstar_growth_net_income = pd.DataFrame([Ticker.__data_list(data[156+length]), Ticker.__data_list(data[158+length])
                                                   , Ticker.__data_list(data[160+length]), Ticker.__data_list(data[162+length])]
                          , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                          , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
        except(ValueError):
            Ticker.__data_list(data[156+length]).append(None)
            self.morningstar_growth_net_income = pd.DataFrame([Ticker.__data_list(data[156+length]), Ticker.__data_list(data[158+length])
                                                   , Ticker.__data_list(data[160+length]), Ticker.__data_list(data[162+length])]
                          , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                          , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_net_income
    
    def __morningstar_growth_eps(self):
        
        data = self.data
        length = self.length
    
        self.morningstar_growth_eps = pd.DataFrame([Ticker.__data_list(data[167+length]), Ticker.__data_list(data[169+length])
                                        , Ticker.__data_list(data[171+length]), Ticker.__data_list(data[173+length])]
                      , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                      , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_eps
        
    def __morningstar_cashflow_ratios(self):
        
        data = self.data
        length = self.length
        
        self.morningstar_cashflow_ratios = pd.DataFrame([Ticker.__data_list(data[187+length]), Ticker.__data_list(data[193+length])
                                             , Ticker.__data_list(data[204+length]), Ticker.__data_list(data[204+length])
                                             , Ticker.__data_list(data[208+length])]
                      , index =['Operating Cash Flow Growth % YOY', 'Free Cash Flow Growth % YOY', 'Cap Ex as a % of Sales'
                                , 'Free Cash Flow/Sales %', 'Free Cash Flow/Net Income']
                      , columns =Ticker.__data_list(data[181+length]))
    
        return self.morningstar_cashflow_ratios
    
    def __morningstar_finhealth_bs(self):
        
        data = self.data
        length = self.length
        
        self.morningstar_finhealth_bs = pd.DataFrame([Ticker.__data_list(data[223+length]), Ticker.__data_list(data[225+length])
                                          , Ticker.__data_list(data[226+length]), Ticker.__data_list(data[229+length])
                                          , Ticker.__data_list(data[232+length]), Ticker.__data_list(data[234+length])
                                          , Ticker.__data_list(data[235+length]), Ticker.__data_list(data[238+length])
                                          , Ticker.__data_list(data[240+length]), Ticker.__data_list(data[242+length])
                                          , Ticker.__data_list(data[244+length]), Ticker.__data_list(data[246+length])
                                          , Ticker.__data_list(data[248+length]), Ticker.__data_list(data[251+length])
                                          , Ticker.__data_list(data[254+length]), Ticker.__data_list(data[256+length])
                                          , Ticker.__data_list(data[259+length]), Ticker.__data_list(data[261+length])
                                          , Ticker.__data_list(data[264+length]), Ticker.__data_list(data[268+length])]
                          , index =['Cash & Short-Term Investments', 'Accounts Receivable', 'Inventory', 'Other Current Assets'
                                    , 'Total Current Assets', 'Net PP&E', 'Intangibles', 'Other Long-Term Assets', 'Total Assets'
                                    , 'Accounts Payable', 'Short-Term Debt', 'Taxes Payable', 'Accrued Liabilities'
                                    , 'Other Short-Term Liabilities', 'Total Current Liabilities', 'Long-Term Debt', 'Other Long-Term Liabilities'
                                    ,'Total Liabilities', "Total Stockholder's Equity", 'Total Liabilities & Equity']
                          , columns = Ticker.__data_list(data[218+length] + ' ' + data[219+length]))
    
        return self.morningstar_finhealth_bs
        
    def __morningstar_finhealth_health(self):
        
        data = self.data
        length = self.length
        
        self.morningstar_finhealth_health = pd.DataFrame([Ticker.__data_list(data[273+length]), Ticker.__data_list(data[275+length])
                                              , Ticker.__data_list(data[277+length]), Ticker.__data_list(data[278+length])]
                          , index =['Current Ratio', 'Quick Ratio', 'Financial Leverage', 'Debt/Equity']
                          , columns = Ticker.__data_list(data[270+length] + ' ' + data[271+length]))
        
        return self.morningstar_finhealth_health
    
        
    def __morningstar_effiency_ratios(self):
        
        data = self.data
        length = self.length
        
        self.morningstar_effiency_ratios = pd.DataFrame([Ticker.__data_list(data[287+length]), Ticker.__data_list(data[289+length])
                                             , Ticker.__data_list(data[291+length]), Ticker.__data_list(data[294+length])
                                             , Ticker.__data_list(data[296+length]), Ticker.__data_list(data[298+length])
                                             , Ticker.__data_list(data[301+length]), Ticker.__data_list(data[303+length])]
                      , index =['Days Sales Outstanding', 'Days Inventory', 'Payables Period', 'Cash Conversion Cycle'
                                , 'Receivables Turnover', 'Inventory Turnover', 'Fixed Assets Turnover', 'Asset Turnover']
                      , columns = Ticker.__data_list(data[284+length]))
    
        return self.morningstar_effiency_ratios
    
    def __data_list(string):
        if '"' in string:
            substrings = []
            for s_quote_mark in string.split('"'):
                if len(s_quote_mark)>0: 
                    if s_quote_mark[0]=="," or s_quote_mark[-1]=="," or s_quote_mark==string:
                        for s_comma in s_quote_mark.split(','):
                            if len(s_comma)>0:
                                substrings.append(s_comma)
                            #else:
                            #    substrings.append(None)
                    else:
                        substrings.append(s_quote_mark)
        else: 
            substrings = string.split(',')
    
            for n, i in enumerate(substrings):
	            if len(substrings[n]) == 0:
		            substrings[n] = None
        
        del substrings[0]
    
        return substrings
    
    def __index(string):
        string = string.split(',')
        return string[0]
    
    ### Nasdaq Summary ###
    def __nasdaq_summary_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/summary?assetclass=stocks", headers=self.headers_standard)
        json = r.json()
        
        json_data_1 = json['data']['summaryData']['Exchange']
        json_data_2 = json['data']['summaryData']['Sector']
        json_data_3 = json['data']['summaryData']['Industry']
        json_data_4 = json['data']['summaryData']['OneYrTarget']
        json_data_5 = json['data']['summaryData']['TodayHighLow']
        json_data_6 = json['data']['summaryData']['ShareVolume']
        json_data_7 = json['data']['summaryData']['AverageVolume']
        json_data_8 = json['data']['summaryData']['PreviousClose']
        json_data_9 = json['data']['summaryData']['FiftTwoWeekHighLow']
        json_data_10 = json['data']['summaryData']['MarketCap']
        json_data_11 = json['data']['summaryData']['PERatio']
        json_data_12 = json['data']['summaryData']['ForwardPE1Yr']
        json_data_13 = json['data']['summaryData']['EarningsPerShare']
        json_data_14 = json['data']['summaryData']['AnnualizedDividend']
        json_data_15 = json['data']['summaryData']['ExDividendDate']
        json_data_16 = json['data']['summaryData']['DividendPaymentDate']
        json_data_17 = json['data']['summaryData']['Yield']
        json_data_18 = json['data']['summaryData']['Beta']
        
        df_1 = json_normalize(json_data_1)
        df_2 = json_normalize(json_data_2)
        df_3 = json_normalize(json_data_3)
        df_4 = json_normalize(json_data_4)
        df_5 = json_normalize(json_data_5)
        df_6 = json_normalize(json_data_6)
        df_7 = json_normalize(json_data_7)
        df_8 = json_normalize(json_data_8)
        df_9 = json_normalize(json_data_9)
        df_10 = json_normalize(json_data_10)
        df_11 = json_normalize(json_data_11)
        df_12 = json_normalize(json_data_12)
        df_13 = json_normalize(json_data_13)
        df_14 = json_normalize(json_data_14)
        df_15 = json_normalize(json_data_15)
        df_16 = json_normalize(json_data_16)
        df_17 = json_normalize(json_data_17)
        df_18 = json_normalize(json_data_18)
        
        df_nasdaq_summary = df_1.append([df_2,df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10, df_11, df_12
                          , df_13, df_14, df_15, df_16, df_17, df_18])
        
        df_nasdaq_summary = df_nasdaq_summary.reset_index(drop=True)
        
        self.nasdaq_summary_df = df_nasdaq_summary.rename(columns={'label':'Label','value':'Value'})
        
        return self.nasdaq_summary_df
    
    ### Nasdaq Dividend History ###
    def __nasdaq_dividend_history_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/dividends?assetclass=stocks", headers=self.headers_standard)
        json = r.json()
        
        json_data = json['data']['dividends']['rows']
        df = json_normalize(json_data)
        json_headers = json['data']['dividends']['headers']
        df_headers = json_normalize(json_headers)
        self.nasdaq_dividend_history_df = df.rename(columns=df_headers.loc[0])
        
        return self.nasdaq_dividend_history_df
    
    ### Nasdaq Historical NOCP ###
    def __nasdaq_historical_nocp_df(self):    
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/historical-nocp?timeframe=y1", headers=self.headers_standard)
        json = r.json()
        
        json_data = json['data']['nocp']['nocpTable']
        df = json_normalize(json_data)
        json_headers = json['data']['headers']
        df_headers = json_normalize(json_headers)
        self.nasdaq_historical_nocp_df = df.rename(columns=df_headers.loc[0])
        
        return self.nasdaq_historical_nocp_df
    
    ### Nasdaq Financials Annual Income Statement ###    
    def __nasdaq_financials_income_statement_y_df(self): 
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        json = r.json()
        
        json_1 = json['data']['incomeStatementTable']['rows']
        df = json_normalize(json_1)
        json_headers_1 = json['data']['incomeStatementTable']['headers']
        df_headers_1 = json_normalize(json_headers_1)
        self.nasdaq_financials_income_statement_df = df.rename(columns=df_headers_1.loc[0])
        
        return self.nasdaq_financials_income_statement_df
    
    ### Nasdaq Financials Annual Balance Statement ###    
    def __nasdaq_financials_balance_sheet_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        json = r.json()
        
        json_2 = json['data']['balanceSheetTable']['rows']
        df = json_normalize(json_2)
        json_headers_2 = json['data']['balanceSheetTable']['headers']
        df_headers_2 = json_normalize(json_headers_2)
        self.nasdaq_financials_balance_sheet_df = df.rename(columns=df_headers_2.loc[0])
        
        return self.nasdaq_financials_balance_sheet_df
    
    ### Nasdaq Financials Annual Cash Flow ###    
    def __nasdaq_financials_cash_flow_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        json = r.json()
        
        json_3 = json['data']['cashFlowTable']['rows']
        df = json_normalize(json_3)
        json_headers_3 = json['data']['cashFlowTable']['headers']
        df_headers_3 = json_normalize(json_headers_3)
        self.nasdaq_financials_cash_flow_df = df.rename(columns=df_headers_3.loc[0])
        
        return self.nasdaq_financials_cash_flow_df
    
    ### Nasdaq Financials Annual Financial Ratios ###    
    def __nasdaq_financials_financials_ratios_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        json = r.json()
        
        json_4 = json['data']['financialRatiosTable']['rows']
        df = json_normalize(json_4)
        json_headers_4 = json['data']['financialRatiosTable']['headers']
        df_headers_4 = json_normalize(json_headers_4)
        self.nasdaq_financials_financials_ratios_df = df.rename(columns=df_headers_4.loc[0])
        
        return self.nasdaq_financials_financials_ratios_df

    ### Nasdaq Financials Quarterly Income Statement ###    
    def __nasdaq_financials_income_statement_q_df(self): 
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        json = r.json()
        
        json_1 = json['data']['incomeStatementTable']['rows']
        df = json_normalize(json_1)
        json_headers_1 = json['data']['incomeStatementTable']['headers']
        df_headers_1 = json_normalize(json_headers_1)
        self.nasdaq_financials_income_statement_df = df.rename(columns=df_headers_1.loc[0])
        
        return self.nasdaq_financials_income_statement_df
    
    ### Nasdaq Financials Quarterly Balance Statement ###    
    def __nasdaq_financials_balance_sheet_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        json = r.json()
        
        json_2 = json['data']['balanceSheetTable']['rows']
        df = json_normalize(json_2)
        json_headers_2 = json['data']['balanceSheetTable']['headers']
        df_headers_2 = json_normalize(json_headers_2)
        self.nasdaq_financials_balance_sheet_df = df.rename(columns=df_headers_2.loc[0])
        
        return self.nasdaq_financials_balance_sheet_df
    
    ### Nasdaq Financials Quarterly Cash Flow ###    
    def __nasdaq_financials_cash_flow_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        json = r.json()
        
        json_3 = json['data']['cashFlowTable']['rows']
        df = json_normalize(json_3)
        json_headers_3 = json['data']['cashFlowTable']['headers']
        df_headers_3 = json_normalize(json_headers_3)
        self.nasdaq_financials_cash_flow_df = df.rename(columns=df_headers_3.loc[0])
        
        return self.nasdaq_financials_cash_flow_df
    
    ### Nasdaq Financials Quarterly Financial Ratios ###    
    def __nasdaq_financials_financials_ratios_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        json = r.json()
        
        json_4 = json['data']['financialRatiosTable']['rows']
        df = json_normalize(json_4)
        json_headers_4 = json['data']['financialRatiosTable']['headers']
        df_headers_4 = json_normalize(json_headers_4)
        self.nasdaq_financials_financials_ratios_df = df.rename(columns=df_headers_4.loc[0])
        
        return self.nasdaq_financials_financials_ratios_df

    ### Nasdaq Earnings Date Earnings Per Share ###
    def __nasdaq_earnings_date_eps_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/eps", headers=self.headers_standard)
        json = r.json()
        
        json_data = json['data']['earningsPerShare']
        self.nasdaq_earnings_date_eps_df = json_normalize(json_data)
        
        return self.nasdaq_earnings_date_eps_df


    ### Nasdaq Earnings Date Quarterly Earnings Surprise Amount ###
    def __nasdaq_earnings_date_surprise_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/earnings-surprise", headers=self.headers_standard)
        
        json = r.json()
        
        json_data = json['data']['earningsSurpriseTable']['rows']
        df = json_normalize(json_data)
        json_headers = json['data']['earningsSurpriseTable']['headers']
        df_headers = json_normalize(json_headers)
        self.nasdaq_earnings_date_surprise_df = df.rename(columns=df_headers.loc[0])
        
        return self.nasdaq_earnings_date_surprise_df
    
    ### Nasdaq Earnings Date Yearly Earnings Forecast ###
    def __nasdaq_earnings_date_yearly_earnings_forecast_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/earnings-forecast", headers=self.headers_standard)
        json = r.json()
        
        json_data = json['data']['yearlyForecast']['rows']
        df = json_normalize(json_data)
        json_headers = json['data']['yearlyForecast']['headers']
        df_headers = json_normalize(json_headers)
        self.nasdaq_earnings_date_yearly_earnings_forecast_df = df.rename(columns=df_headers.loc[0])
        
        return self.nasdaq_earnings_date_yearly_earnings_forecast_df


    ### Nasdaq Earnings Date Quarterly Earnings ###
    def __nasdaq_earnings_date_quarterly_earnings_forecast_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/earnings-forecast", headers=self.headers_standard)
        json = r.json()
        
        json_data = json['data']['quarterlyForecast']['rows']
        df = json_normalize(json_data)
        json_headers = json['data']['quarterlyForecast']['headers']
        df_headers = json_normalize(json_headers)
        self.nasdaq_earnings_date_quarterly_earnings_forecast_df = df.rename(columns=df_headers.loc[0])
        
        return self.nasdaq_earnings_date_quarterly_earnings_forecast_df
    
    ### Price/Earnings & PEG Ratios Forecast Price/Earnings ###
    def __forecast_pe_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/peg-ratio", headers=self.headers_standard)
        json = r.json()
        
        json_data_forecast_pe = json['data']['per']['peRatioChart']
        df_forecast_pe = json_normalize(json_data_forecast_pe)
        self.forecast_pe_df = df_forecast_pe.rename (columns={'x':'Date', 'y':'Price/Earnings Ratio'})
        
        return self.forecast_pe_df
    
    ### Price/Earnings & PEG Ratios Forecast P/E Growth Rates ###
    def __forecast_gr_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/peg-ratio", headers=self.headers_standard)
        json = r.json()
        
        json_data_forecast_gr = json['data']['gr']['peGrowthChart']
        df_forecast_gr = json_normalize(json_data_forecast_gr)
        self.forecast_gr_df = df_forecast_gr.rename (columns={'x':'Date', 'y':'Ratio', 'z':'Type'})
        
        return self.forecast_gr_df
    
    ### Price/Earnings & PEG Ratios Forecast PEG Ratio ###
    def __forecast_peg_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/peg-ratio", headers=self.headers_standard)
        json = r.json()
        
        json_data_forecast_peg = json['data']['pegr']
        df_forecast_peg = json_normalize(json_data_forecast_peg)
        self.forecast_peg_df = df_forecast_peg.rename (columns={'pegValue':'Forward PEG Ratio'})
        
        return self.forecast_peg_df
    
    ### Historical Data Stocks###
    def __nasdaq_historical_data_stock_df(self):
        from datetime import datetime
        datum = datetime.today().strftime('%Y-%m-%d')
        
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/historical?assetclass=stocks&fromdate=2011-09-26&limit=9999&todate={datum}", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['tradesTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['tradesTable']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_historical_data_stock_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_historical_data_stock_df = None
        
        return self.nasdaq_historical_data_stock_df
    
    ### Historical Data ETF###
    def __nasdaq_historical_data_etf_df(self):
        from datetime import datetime
        datum = datetime.today().strftime('%Y-%m-%d')
        
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/historical?assetclass=etf&fromdate=2011-09-26&limit=9999&todate={datum}", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['tradesTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['tradesTable']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_historical_data_etf_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_historical_data_etf_df = None
        
        return self.nasdaq_historical_data_etf_df
    
    ### Yahoo Finance Statistics ###
    def __yahoo_statistics_df(self):
        url = f'https://finance.yahoo.com/quote/{self.ticker}/key-statistics'
        
        with requests.session():
            
            page = requests.get(url, headers = self.headers_standard)
            page = BeautifulSoup(page.content, 'html.parser')
            table = page.find_all('td', {'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})
                   
            arrays = [
                np.array(["Valuation Measures", "Valuation Measures", "Valuation Measures", "Valuation Measures"
                          , "Valuation Measures", "Valuation Measures", "Valuation Measures", "Valuation Measures"
                          , "Valuation Measures"
                          , "Stock Price History", "Stock Price History","Stock Price History", "Stock Price History"
                          , "Stock Price History", "Stock Price History","Stock Price History"
                          , "Share Statistics", "Share Statistics","Share Statistics","Share Statistics"
                          , "Share Statistics", "Share Statistics","Share Statistics","Share Statistics"
                          , "Share Statistics", "Share Statistics","Share Statistics","Share Statistics"
                          , "Dividends & Splits", "Dividends & Splits","Dividends & Splits","Dividends & Splits"
                          , "Dividends & Splits", "Dividends & Splits","Dividends & Splits","Dividends & Splits"
                          , "Dividends & Splits", "Dividends & Splits"
                          , "Fiscal Year", "Fiscal Year"
                          , "Profitability", "Profitability"
                          , "Management Effectiveness", "Management Effectiveness"
                          , "Income Statement", "Income Statement","Income Statement","Income Statement"
                          , "Income Statement", "Income Statement","Income Statement","Income Statement"
                          , "Balance Sheet", "Balance Sheet","Balance Sheet","Balance Sheet"
                          , "Balance Sheet", "Balance Sheet"
                          , "Cash Flow Statement", "Cash Flow Statement"
                          ]),
                
                np.array(["Market Cap (intraday)", "Enterprise Value", "Trailing P/E", "Forward P/E"
                          , "PEG Ratio (5 yr expected)", "Price/Sales (ttm)", "Price/Book (mrq)"
                          , "Enterprise Value/Revenue", "Enterprise Value/EBITDA"
                          , "Beta (5Y Monthly)", "52-Week Change", "S&P500 52-Week Change", "52 Week High"
                          , "52 Week Low", "50-Day Moving Average", "200-Day Moving Average"
                          , "Avg Vol (3 month)", "Avg Vol (10 day)", "Shares Outstanding"
                          , "Implied Shares Outstanding", "Float", "% Held by Insiders"
                          , "% Held by Institutions", "Shares Short", "Short Ratio"
                          , "Short % of Float", "Short % of Shares Outstanding"
                          , "Shares Short (prior month)"
                          , "Forward Annual Dividend Rate", "Forward Annual Dividend Yield"
                          , "Trailing Annual Dividend Rate", "Trailing Annual Dividend Yield"
                          , "5 Year Average Dividend Yield", "Payout Ratio", "Dividend Date"
                          , "Ex-Dividend Date", "Last Split Factor", "Last Split Date"
                          , "Fiscal Year Ends", "Most Recent Quarter (mrq)"
                          , "Profit Margin", "Operating Margin (ttm)"
                          , "Return on Assets (ttm)", "Return on Assets (ttm)"
                          , "Revenue (ttm)", "Revenue Per Share (ttm)", "Quarterly Revenue Growth (yoy)"
                          , "Gross Profit (ttm)", "EBITDA ", "Net Income Avi to Common (ttm)"
                          , "Diluted EPS (ttm)", "Quarterly Earnings Growth (yoy)"
                          , "Total Cash (mrq)", "Total Cash Per Share (mrq)", "Total Debt (mrq)"
                          , "Total Debt/Equity (mrq)", "Current Ratio (mrq)", "Book Value Per Share (mrq)"
                          , "Operating Cash Flow (ttm)", "Levered Free Cash Flow (ttm)"
                          ]),]
    
            s = pd.DataFrame([table[0].text.strip(),table[1].text.strip(),table[2].text.strip(), table[3].text.strip()
                          , table[4].text.strip(),table[5].text.strip(),table[6].text.strip(), table[7].text.strip()
                          , table[8].text.strip(),table[9].text.strip(),table[10].text.strip(), table[11].text.strip()
                          , table[12].text.strip(),table[13].text.strip(),table[14].text.strip(), table[15].text.strip()
                          , table[16].text.strip(),table[17].text.strip(),table[18].text.strip(), table[19].text.strip()
                          , table[20].text.strip(),table[21].text.strip(),table[22].text.strip(), table[23].text.strip()
                          , table[24].text.strip(),table[25].text.strip(),table[26].text.strip(), table[27].text.strip()
                          , table[28].text.strip(),table[29].text.strip(),table[30].text.strip(), table[31].text.strip()
                          , table[32].text.strip(),table[33].text.strip(),table[34].text.strip(), table[35].text.strip()
                          , table[36].text.strip(),table[37].text.strip(), table[38].text.strip(),table[39].text.strip()
                          , table[40].text.strip(),table[41].text.strip(), table[42].text.strip(),table[43].text.strip()
                          , table[44].text.strip(),table[45].text.strip(), table[46].text.strip(),table[47].text.strip()
                          , table[48].text.strip(),table[49].text.strip(), table[50].text.strip(),table[51].text.strip()
                          , table[52].text.strip(),table[53].text.strip(), table[54].text.strip(),table[55].text.strip()
                          , table[56].text.strip(),table[57].text.strip(), table[58].text.strip(),table[59].text.strip()
                          ]
                          , index=arrays
                          , columns = [self.ticker + ' Yahoo Statistics'])
            
            s = s.loc[:,'NVDA Yahoo Statistics'].replace(['N/A'],np.nan)
            
            self.yahoo_statistics_df = s.to_frame(name= self.ticker + ' Yahoo Statistics')
        
        return self.yahoo_statistics_df
    
class StockExchange:

    def __init__(self, stockexchange):
        self.stockexchange = stockexchange
        
    def __repr__(self):
        return(self.stockexchange)
        
    def __str__(self):
        return(self.stockexchange)
    
    @property
    def nasdaq(self):
        return self.__df_stockexchange()
    
    def __df_stockexchange(self):
        
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        }
        
        r = requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true", headers=headers)
        
        json = r.json()
               
        json_data = json['data']['rows']
        df = json_normalize(json_data)
        json_headers = json['data']['headers']
        df_headers = json_normalize(json_headers)
        df_nasdaq_stockexchange = df.rename(columns=df_headers.loc[0])
        
        return df_nasdaq_stockexchange