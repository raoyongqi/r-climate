import geopandas as gpd
import json

# 读取 GeoJSON 文件
grasslands_geojson_file = '/home/r/Desktop/r-climate/data/clipped_data.geojson'
grasslands_gdf = gpd.read_file(grasslands_geojson_file)

# 筛选出值等于 10 的 Grasslands (草地)
grasslands_gdf_filtered = grasslands_gdf[grasslands_gdf['value'] == 10]

# 保存筛选后的数据为新的 GeoJSON 文件
filtered_geojson_file = '/home/r/Desktop/r-climate/data/filtered_grasslands.geojson'
grasslands_gdf_filtered.to_file(filtered_geojson_file, driver='GeoJSON')

print(f"筛选后的 GeoJSON 文件已保存到: {filtered_geojson_file}")

