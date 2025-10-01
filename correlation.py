import os
import json
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def getdf(name):
	with open(name,"r") as stack_history:
		stack=json.load(stack_history)['closingPriceChartData']
	
	stack_data ={
		'Date': [],
		'Open': [], 
		'High': [], 
		'Low': [],
		'Close': [], 
		'Volume': [],
		'Color' : []
		}
	basetime_sec= -17887996800
	basedate = datetime(2024, 5, 15, 0, 0, 0)
	
	for day in stack:
		stack_data['Date'].append(basedate + timedelta(seconds= day['dEven']-basetime_sec))
		stack_data['Open'].append(day['priceFirst'])
		stack_data['Close'].append(day['pDrCotVal'])
		stack_data['High'].append(day['priceMax'])
		stack_data['Low'].append(day['priceMin'])
		stack_data['Volume'].append(day['qTotTran5J'])
		stack_data['Color'].append('crimson' if day['priceFirst']>day['pDrCotVal'] else 'mediumseagreen' )
	
	df=pd.DataFrame(stack_data)
	df['Date'] = pd.to_datetime(df['Date'])
	
	return df
	


path = 'history'
	
files = [path+'/'+f for f in os.listdir(path)]
output = open('correlation_data_try02.txt', 'a')
	
print(files[0])
correlations = []
for i in range(0,896):
	print(i)
	df1 = getdf(files[i])
	for j in range(i+1,896):

		df2 = getdf(files[j])

		merged_df = pd.merge(df1[-100:][['Date', 'Close']], df2[-100:][['Date', 'Close']], on='Date', how='outer', suffixes=('_df1', '_df2'))
		merged_df.set_index('Date', inplace=True)
		
		correlation = merged_df['Close_df1'].corr(merged_df['Close_df2'])

		if(-1<=correlation<=1):
			correlations.append((correlation,files[i],files[i]));
			output.write(f"({correlation} , {files[i]} , {files[j]})\n")
			output.write('\n')

correlations.sort()


print(correlations[-5:])
print(correlations[:5])