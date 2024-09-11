import geopandas as gpd
import json

# 读取 GeoJSON 文件
grasslands_geojson_file = '/home/r/Desktop/r-climate/data/clipped_data.geojson'
grasslands_gdf = gpd.read_file(grasslands_geojson_file)

# 筛选出值等于 10 的 Grasslands (草地)
grasslands_gdf_filtered = grasslands_gdf[grasslands_gdf['value'] == 10]

# 将筛选后的 GeoDataFrame 转换为 GeoJSON 格式
grasslands_geojson_filtered = grasslands_gdf_filtered.to_json()

# 将 GeoJSON 字符串解析为 Python 字典
geojson_dict = json.loads(grasslands_geojson_filtered)

# 提取 'features' 部分
features = geojson_dict['features']

# 将 'features' 部分转换为普通 JSON 格式
filtered_json = json.dumps(features, indent=4)

# 保存普通 JSON 格式数据到文件
filtered_json_file = '/home/r/Desktop/r-climate/data/grasslands_filtered.json'
with open(filtered_json_file, 'w') as f:
    f.write(filtered_json)

print(f"Filtered JSON data saved to {filtered_json_file}")
