import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

df_citywise = pd.read_csv("Citypairwise Quarterly International  Air Traffic To And From The Indian Territory.csv", error_bad_lines=False)
df_citywise = df_citywise.iloc[:, :-3]


df_citywise['TOTAL TRAFFIC'] = df_citywise['PASSENGERS FROM CITY1 TO CITY2'] + df_citywise['PASSENGERS FROM CITY2 TO CITY1']


df_citywise_cumulative_traffic = df_citywise.groupby(['CITY1', 'CITY2'])['TOTAL TRAFFIC'].sum().reset_index()

AVG_PASSENGERS_PER_FLIGHT = 240
df_citywise_cumulative_traffic ['nb_flights'] = round(df_citywise_cumulative_traffic ['TOTAL TRAFFIC'] / AVG_PASSENGERS_PER_FLIGHT)

geolocator = Nominatim()
geolocator.timeout = 180

location = geolocator.geocode("ABUDHABI")
print(str(location.latitude) + ', ' + str(location.longitude))
print(df_citywise_cumulative_traffic.head(10))

location_dict = {}

dep_cities = df_citywise_cumulative_traffic['CITY1'].unique()
dep_cities = np.append(dep_cities, df_citywise_cumulative_traffic['CITY2'].unique())


for dep_city in dep_cities:
    print ('Geocoding - ' + dep_city)
    location = geolocator.geocode(dep_city)
    if location is not None:
        location_dict[dep_city] = (location.latitude, location.longitude)
    else:
        print('Failed - ' + dep_city)
        location_dict[dep_city] = location_dict['ABUDHABI']
print(location_dict)

df_citywise_cumulative_traffic['dep_lat'] = df_citywise_cumulative_traffic['CITY1'].apply(lambda city: location_dict[city][0])
df_citywise_cumulative_traffic['dep_lon'] = df_citywise_cumulative_traffic['CITY1'].apply(lambda city: location_dict[city][1])
df_citywise_cumulative_traffic['arr_lat'] = df_citywise_cumulative_traffic['CITY2'].apply(lambda city: location_dict[city][0])
df_citywise_cumulative_traffic['arr_lon'] = df_citywise_cumulative_traffic['CITY2'].apply(lambda city: location_dict[city][1])

df_citywise_cumulative_traffic.to_csv('flight_data', index=False, encoding='utf-8')

print(df_citywise_cumulative_traffic.head(50))