import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import numpy as np
from scipy.integrate import quad


data = pd.read_csv('S_strip_4_eald.csv')
#adding column names to the data
data.columns = ['Voltage (V)', 'Current (I/uA)']
current = data['Current (I/uA)']
volts = data['Voltage (V)']
print(data.head())

poly = PolynomialFeatures(degree=44)
X = poly.fit_transform(volts[:, np.newaxis])

model = LinearRegression()
model.fit(X, current)

y_pred = model.predict(X)

plt.plot(volts, current, 'b.')
plt.plot(volts, y_pred, 'r')
plt.show()

value = float(input('Enter an x-coordinate: '))
value_2 = float(input('Enter an x-coordinate: '))

idx = data.loc[data['Voltage (V)'] == value].index[0]
idx_2 = data.loc[data['Voltage (V)'] == value_2].index[0]

x_0 = volts.iloc[idx]
y_0 = current.iloc[idx]

x_1 = volts.iloc[idx_2]
y_1 = current.iloc[idx_2]

m = (y_1 - y_0) / (x_1 - x_0)
b = y_0 - m * x_0

x = [value_2, value]
y = [m * xi + b for xi in x]

plt.plot(x, y)
plt.plot([x_0, x_1], [y_0, y_1], 'rx')


#calculate the area
area, _ = quad(lambda x: abs(y_pred[0] - (m * x + b)), x_0, x_1)
print(f'The area of the region is {area}')

charge_C = area * 0.050
num_elec = charge_C / 1.602E-19


print(f'The charge (C) is {charge_C} and \n the number of electrons involved is {num_elec}')
#plt.savefig('Cd_strip_4_eald_region.png')
plt.show()

