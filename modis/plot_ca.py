import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 读取 GeoJSON 数据
geojson_file_path = '/home/r/Desktop/r-climate/geojson/中华人民共和国.json'
gdf_geojson = gpd.read_file(geojson_file_path)

# 读取 Shapefile 数据
shp_file_path = '/home/r/Desktop/r-climate/data/clipped_data.geojson'
gdf_shp = gpd.read_file(shp_file_path)

# 筛选出值等于 10 的 Grasslands (草地)
if 'value' in gdf_shp.columns:
    grasslands_gdf = gdf_shp[gdf_shp['value'] == 10]
else:
    raise KeyError("The column 'value' does not exist in the shapefile data.")

# 定义 Albers 投影坐标系
albers_proj = ccrs.AlbersEqualArea(
    central_longitude=105,
    central_latitude=35,
    standard_parallels=(25, 47)
)

# 创建绘图对象
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': albers_proj})

# 转换 GeoJSON 数据的坐标系到自定义投影坐标系
if gdf_geojson.crs != albers_proj:
    gdf_geojson = gdf_geojson.to_crs(albers_proj)

# 转换 Shapefile 数据的坐标系到自定义投影坐标系
if grasslands_gdf.crs != albers_proj:
    grasslands_gdf = grasslands_gdf.to_crs(albers_proj)

# 绘制转换后的 GeoJSON 数据
gdf_geojson.plot(ax=ax, edgecolor='black', facecolor='white', label='GeoJSON Data')

# 绘制筛选后的 Grasslands 数据
grasslands_gdf.plot(ax=ax, edgecolor='green', facecolor='green', linewidth=2, alpha=0.5, label='Grasslands (value=10)')

# 添加标题
plt.title('Filtered Grasslands and GeoJSON Data with Custom Projection')

# 添加图例
legend_patches = [
    mpatches.Patch(color='green', label='Grassland (value=10)'),
    mpatches.Patch(color='white', edgecolor='black', label='Other Areas'),
]
plt.legend(handles=legend_patches)

# 设置坐标轴标签
ax.set_xlabel('Easting (meters)')
ax.set_ylabel('Northing (meters)')

# 添加经纬度网格线
gridlines = ax.gridlines(draw_labels=True, color='gray', linestyle='--', alpha=0.5)
gridlines.xlabel_style = {'size': 10}
gridlines.ylabel_style = {'size': 10}
# 隐藏右边和上边的网格线标签
gridlines.top_labels = False
gridlines.right_labels = False

# 保存图形到文件
output_file_path = '/home/r/Desktop/r-climate/data/shapefile_overlay_cartopy.png'
plt.savefig(output_file_path, dpi=300, bbox_inches='tight')

# 显示图形
plt.show()
