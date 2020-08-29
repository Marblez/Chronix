import hmmlearn
import talib
import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.metrics import mean_squared_error
import Library
import FirebaseClient

def main():
	####################################################
	data = Library.get_all_binance("ETHUSDT", "5m", save = True)
	step_range = range(30, 151, 10) 
	windows = range(50, 251, 10)
	compression = 240 # 20 hours
	regimes = 4
	####################################################
	# Preparing Data
	close = np.array(data.iloc[:,3].astype(float), np.float)[-279564:] # Jan 1 2018 - Present
	obs = []
	temp = []
	for i in range(0, len(close)):
		temp.append(close[i])
		if len(temp) == compression:
			today = [((temp[-1] - temp[0] )/ temp[0]), mean_squared_error(temp, [sum(temp) / len(temp)] * len(temp))]
			obs.append(today)
			temp = []
	####################################################
	# Configuring Data, Training, Simulation, Logging
	for step in step_range:
		for window in windows:
			balance = simulation(regimes, obs, step, window)
			#FirebaseClient.log(("HMM1:" + str(step) + ":" + str(window)), balance)

####################################################
# Simulation Code
def simulation(regimes, obs, step, window):
	model = hmm.GaussianHMM(n_components = regimes, covariance_type="full", n_iter = step);
	training = obs[(250-window):250]
	model.fit(training)
	balances = [10000]
	position = [0]
	for i in range(251, len(obs)):
		training.append(obs[i])
		training.pop(0)
		if i % 10 == 0:
			model.fit(training)

		regime_returns = regime_returns()
		transmat = model.transmat_
		prediction = model.predict(training)[-1]

		balances.append()
	return balances

def regime_returns():


main();