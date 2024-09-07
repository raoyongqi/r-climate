import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# 读取 Grasslands GeoJSON 文件
grasslands_geojson_file = 'C:/Users/r/desktop/modis/data/clipped_data.geojson'
grasslands_gdf = gpd.read_file(grasslands_geojson_file)

# 筛选出值等于 10 的 Grasslands (草地)
grasslands_gdf = grasslands_gdf[grasslands_gdf['value'] == 10]

# 读取国界线 GeoJSON 文件
borders_geojson_file = 'C:/Users/r/desktop/modis/geojson/CN-border-L1.geojson'
borders_gdf = gpd.read_file(borders_geojson_file)

# 检查数据
print(grasslands_gdf.head())
print(borders_gdf.head())

# 定义颜色
grassland_color = '#7CFC00'  # Grasslands color
border_color = '#000000'     # Border color

# 创建图例标签
legend_patches = [Patch(color=grassland_color, label='Grasslands'),
                  Patch(color=border_color, label='Borders')]

# 绘制数据
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制 Grasslands 数据
grasslands_gdf.plot(ax=ax, color=grassland_color)

# 绘制 Borders 数据
borders_gdf.plot(ax=ax, color=border_color, linewidth=1)

# 设置标题和标签
ax.set_title('Grasslands and Borders from GeoJSON Files')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# 添加图例
ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), title='Categories')

plt.show()
