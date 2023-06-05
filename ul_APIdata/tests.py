import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# List of coordinates (latitude, longitude)
coordinates = [(47.61092679999999, -122.3446324), (37.7749, -122.4194), (40.7128, -74.0060)]

# Create a DataFrame
df = pd.DataFrame(coordinates, columns=['Latitude', 'Longitude'])

# Create a new column for the geometry (Shapely Points)
df['geometry'] = df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)

# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# Display the GeoDataFrame
print(gdf)

zones=gdf
# Assume 'zones' is a GeoDataFrame with the state plane zone boundaries
# and each zone has a 'zone_id' attribute
joined = gpd.sjoin(gdf, zones, how='left', op='within')

# The 'zone_id' of the zone each point falls within is now joined to the points GeoDataFrame
print(joined['zone_id'])
