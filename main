# (c) Mikal Rian 2025
#
#import streamlit as st
import altair as alt
import numpy as np

def np_XY_table_to_chart_data(table, namelist, namelist_label = 'Type', x_offset=1):
	len_Y = table.shape[0]
	len_X = table.shape[1]

	D = []

	for i in range(len_Y):
		for j in range(len_X):
			d = { 
				namelist_label: namelist[i], 
				'x': j + x_offset,
				'y': table[i][j]
			}
			D.append(d)

	return D

def chart(data, namelist, category_name, x_range, y_min=0, y_max=100, tickcount=12, colours=None, title=''):
	#domain =  [0.5, 0.6, 0.7, 0.8, 0.9]
	#range_ = ['#9cc8e2', '#9cc8e2', 'red', '#5ba3cf', '#125ca4']
	#category_name="Type:N"
	#import streamlit as st
	#st.write(tickcount)

	# create default range of colours if None

	c = (
		alt.Chart(alt.Data(values=data))
		.mark_line()
		.encode(
		    #x="x:O",
		    x = alt.X("x:O", axis=alt.Axis(tickCount=tickcount)),# scale=alt.Scale(domain=np.arange(0, 120, 12), type="ordinal"), axis=alt.Axis(tickCount=tickcount)), 
		    #x=alt.X("x:O", scale=alt.Scale(domain=list(x_range)), axis=alt.Axis(values=list(x_range))),
		    y = alt.Y('y:Q', scale=alt.Scale(domain=(y_min, y_max))),
		    color = alt.Color(f'{category_name}:N', scale=alt.Scale(domain=namelist, range=colours))  # scheme="dark2" or viridis, magma, dark2, inferno
		).properties(title=title)	
	   	).configure_axis(
	   		grid=False
	   	).configure_view(
	   		stroke=None 	# Borders
	)
	return c

if __name__ == "__main__":
	table = np.array([[1, 2, 3], [11, 15, 16], [20, 30, 40]])
	print(table)

	category_name = 'Investment cat'

	namelist = ['Real estate', 'Stocks','suns']
	chart_data = np_XY_table_to_chart_data(table, namelist, namelist_label=category_name)
	print(chart_data)
	c = chart(chart_data, category_name, y_max=100)

	c.show()

	st.altair_chart(c, use_container_width=True) # theme="streamlit" throws error
