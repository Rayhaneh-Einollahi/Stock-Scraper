import numpy as np
import json
from datetime import datetime, timedelta
import pandas as pd
import os



def get_slope(x ,y ):
	n = len(x)
	if(n==0) :
		return 1.7

	sum_x = np.sum(x)
	sum_y = np.sum(y)
	sum_x2 = np.sum(x**2)
	sum_xy = np.sum(x * y)

	slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
	return slope
	
	
def getdata(name):
	with open(name,"r") as stack_history:
		stack=json.load(stack_history)['closingPriceChartData']
	
	stack_data ={
		'Date': [],
		'Close': [], 
		}
	basetime_sec= -17887996800
	basedate = datetime(2024, 5, 15, 0, 0, 0)
	
	for day in stack:
		stack_data['Date'].append((day['dEven']-basetime_sec)/3600/24)
		stack_data['Close'].append(day['pDrCotVal'])
	
	return stack_data
	
	
	
path = 'history'
files = [f for f in os.listdir(path)]

trader = []
holder = []
for i in range(0,896):
	data = getdata(path+'/'+files[i])

	s1 = get_slope(np.array(data['Date'][-14:]) , np.array(data['Close'][-14:]))
	s2 = get_slope(np.array(data['Date'][-90:]) , np.array(data['Close'][-90:]))
	
	if s1>2 :
		trader.append( files[i][:-5])
	if 0<s2 <1.5:
		holder.append(files[i][:-5])

with open("holder.json", "w") as out:
	json.dump(holder,out)
with open("trader.json", "w") as out:
	json.dump(trader,out)
		
	