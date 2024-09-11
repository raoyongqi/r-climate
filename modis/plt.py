import geopandas as gpd
import matplotlib.pyplot as plt

# 读取 GeoJSON 文件
gdf = gpd.read_file('/home/r/Desktop/r-climate/data/clipped_data.geojson')

# 创建一个绘图对象
fig, ax = plt.subplots(figsize=(10, 10))

# 绘制地理数据
gdf.plot(ax=ax, color='blue', edgecolor='black')

# 设置标题
ax.set_title('GeoJSON Data Visualization')

# 如果在没有 GUI 支持的环境中运行，将图形保存到文件
output_file = '/home/r/Desktop/r-climate/data/clipped_data_visualization.png'
fig.savefig(output_file)

# 在 GUI 支持的环境中显示图形
plt.show()
