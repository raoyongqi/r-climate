import pypyodbc
import pandas as pd
from shapely.geometry import Point, mapping
import fiona
from fiona.crs import from_epsg

# Path to your .mdb file
mdb_path = 'HWSD/HWSD.mdb'

# Connect to the .mdb file using pypyodbc
conn_str = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={mdb_path};"
conn = pypyodbc.connect(conn_str)

# List all tables in the database
cursor = conn.cursor()
cursor.execute("SELECT name FROM MSysObjects WHERE type=1 AND flags=0")
tables = [table[0] for table in cursor.fetchall()]

# Assuming the data you need is in the first table
table_name = tables[0]

# Read the data into a pandas DataFrame
query = f"SELECT * FROM {table_name}"
df = pd.read_sql(query, conn)
conn.close()

# Convert to GeoJSON format
geojson_data = []
for _, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        point = Point(row['longitude'], row['latitude'])
        geojson_feature = {
            'type': 'Feature',
            'geometry': mapping(point),
            'properties': row.drop(labels=['latitude', 'longitude']).to_dict()
        }
        geojson_data.append(geojson_feature)

# Define the schema of the Shapefile
schema = {
    'geometry': 'Point',
    'properties': {k: 'str' for k in df.columns if k not in ['latitude', 'longitude']}
}

# Write the data to a Shapefile
with fiona.open('output.shp', 'w', driver='ESRI Shapefile', schema=schema, crs=from_epsg(4326)) as shp:
    for feature in geojson_data:
        shp.write({
            'geometry': feature['geometry'],
            'properties': feature['properties']
        })
