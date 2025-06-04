# (c) Mikal Rian 2025
# 
# To do: Include valuation (growth) of real estate → the price will go up over time, adding x months to n_months (time to save).
# Note: We're rounding down the floats with int(x)
#
import streamlit as st
import numpy as np
import pandas as pd
import graph_altair as graph
from graph_altair import *
st.set_page_config(layout="wide")

def get_r(yr):
	r = np.e**(np.log((1+yr))/12)
	return r

def geometric_series_plus_more(start, end, N, monthly, yearly_rate):
	y = [0 for i in range(N)]
	n = end-start
	r = np.e**(np.log((1+yearly_rate))/12)
	for i in range(start, end):
		n = i - start + 1 + 1 # We want n to start on 2, because we want the first month with investment to also compound (we invest at 00:01 the first day, and read the result at 23:59 the last day).
		a = monthly * (1-r**n) / (1-r)
		a -= monthly
		y[i] = a
	for i in range(end, N):
		y[i] = y[i-1] * r
	return y

def geometric_series(n, start_value=0, repeating_amount=0, periodic_rate=1):
	r = periodic_rate
	if n == 0:
		return []
	y = [0 for i in range(n)]
	if start_value == 0:
		start_value = repeating_amount
	y[0] = start_value * periodic_rate #+ repeating_amount * periodic_rate
	if r == 1:  # Makes .../(1-r) zero division.
		for i in range(1, n):
			y[i] = start_value * periodic_rate + repeating_amount * i
	else:
		#for i in range(0, n):
		#	m = i + 2
		#	a = repeating_amount * (1-r**m) / (1-r)
		#	a -= repeating_amount
		#	y[i] = a
		for i in range(1, n):
			#y[i] = (y[i-1] + repeating_amount) * periodic_rate
			y[i] = y[i-1] * periodic_rate + repeating_amount
	return y

#k = geometric_series(10, 1, 0, 1.07)
#k = geometric_series(10, 1, 0, 1.07)
#print(k); exit()

def compounding(start_value, n, periodic_rate):
	y = [0 for i in range(n)]
	r = periodic_rate
	y[0] = start_value * periodic_rate
	for i in range(1, n):
		y[i] = y[i-1] * r
	return y

def get_debt(i, P, n, extra=0):
	r = i/12
	if i == 0:
		return P
	else:
		try:
			monthly_installments = P * (r*(1 + r)**n) / ((1 + r)**n - 1)
		except Exception as e:
			#monthly_installments = (capital_house - capital_goal) / n
			raise e
		return monthly_installments * n


N = 480
real_estate, space0, stocks, space1, display = st.columns([2, 1, 2, 1, 7])

#Capital = st.sidebar.number_input('Starting capital', min_value=0, value=1, key='start_capital')

with real_estate:
	st.write('Real estate')
	Capital = st.number_input('Starting capital', min_value=0, value=100, key='start_capital')
	monthly_savings = st.number_input('Monthly investments', min_value=0, value=0, key='monthly_savings')

with stocks:
	st.write('Stocks')
	Capital0 = st.number_input('Starting capital', min_value=0, value=Capital, key='start_capital0', disabled=True)
	monthly_invest0 = st.number_input('Monthly investments', min_value=0, value=0, key='monthly_invest0', disabled=False)
	percent_growth = st.slider('\\% growth stocks', min_value=-5, max_value=15, value=4, step=1, key='g_invest')
	rate_growth = percent_growth/100 + 1
	rate_growth = np.e**(np.log(rate_growth)/12)
	realisation_monthly = st.number_input('Monthly take (realisation)', min_value=0, value=0, disabled=False, key='realisation_monthly')

with stocks:
	st.divider()
	display_N = st.selectbox('Display months', [i for i in range(120, 481, 120)], index=1)  # + 12
	display_N = display_N if display_N <= N else N

with real_estate:
	percent_growth_real_invest = st.slider('\\% growth stocks', min_value=-5, max_value=15, value=percent_growth, step=1, key='g_real_and_invest', disabled=True)
	rate_growth_IR = percent_growth_real_invest/100 + 1
	rate_growth_IR = np.e**(np.log(rate_growth_IR)/12)

	rent_income = st.number_input('Rental income', min_value=0, key='rent_income')
	percent_growth_real_estate = st.slider('\\% growth of asset', min_value=-5, max_value=15, value=1, step=1, key="g_real_estate")
	rate_growth_realestate = percent_growth_real_estate/100 + 1
	rate_growth_realestate = np.e**(np.log(rate_growth_realestate)/12)




# Future projection, real estate
capital_real_estate = [Capital * rate_growth_realestate**(i+1) for i in range(N)]
capital_real_estate_incomes = geometric_series(n=N, repeating_amount=monthly_savings + rent_income, periodic_rate=rate_growth_IR)
capital_R = [a + b for a, b in zip(capital_real_estate, capital_real_estate_incomes)]

# Future projection, stocks
capital_stocks = [Capital * rate_growth**(i+1) for i in range(N)]
realisations = geometric_series(n=N, repeating_amount = realisation_monthly, periodic_rate=rate_growth) 
capital_stock_savings = geometric_series(n=N, repeating_amount=monthly_invest0, periodic_rate=rate_growth)
capital_I = [a + b - c for a, b, c in zip(capital_stocks, capital_stock_savings, realisations)]


with display:
	avg = np.arange(len(capital_I)).astype('float32')
	avg[:] = 0

	table = np.array([capital_R[:display_N], capital_I[:display_N]])
	namelist = ['Real estate', 'Stocks']
	category_name = 'Investment type'
	colours = ['blue', 'red', '#5ba3cf', '#125ca4'] # ['#9cc8e2', '#9cc8e2', 'red', '#5ba3cf', '#125ca4']
	chart_data = np_XY_table_to_chart_data(table, namelist, namelist_label=category_name, x_offset=1)
	y_max = np.max(table)
	y_min = np.min(table)
	y_min = y_min if y_min < 0 else y_min*.9
	x_range = range(table.shape[1])
	c = chart(chart_data, namelist, category_name, x_range, y_min=y_min, y_max=y_max*1.1, tickcount=3, colours=colours, title='')



#	data = pd.DataFrame({
#	    'x': range(0, display_N),
#	    'a: Real (+extra pay, invest) *': capital_R,
#	    'c: Real (+invest) **': capital_I,
#	})
#	data.set_index('x', inplace=True)
	st.subheader("Properties or stocks?")
	# Display graphs
	st.altair_chart(c, use_container_width=True) # theme="streamlit" throws error

	st.write('Highest value, real estate:', int(np.max(table[0,:])))
	st.write('Highest value, stocks:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', int(np.max(table[1,:])))
	#st.write("With extra repayments, your loan repayment will take", n_months_duration_debt0, "months, and total cost will be ", round(total_cost_fast_repay,2))
	#st.write("With normal repayments, the loan repayment will take", n_months_debt, "months, and total cost will be ", round(total_cost_regular,2))
