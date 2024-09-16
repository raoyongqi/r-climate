from osgeo import gdal
import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
from rasterio.transform import from_origin
import rasterio.features

# 替换为实际的 HDF 文件路径
hdf_file = '/home/r/Desktop/r-climate/data/MCD12C1.A2020001.061.2022172062638.hdf'
subdataset_name = 'HDF4_EOS:EOS_GRID:"{}":MOD12C1:Majority_Land_Cover_Type_1'.format(hdf_file)

# 打开 HDF 文件中的图层
dataset = gdal.Open(subdataset_name)
band = dataset.GetRasterBand(1)

# 读取图层数据
data = band.ReadAsArray()

# 打印数据类型以确认
print(f"Original data type: {data.dtype}")

# 确保数据类型符合要求
if data.dtype not in [np.int16, np.int32, np.uint8, np.uint16, np.float32]:
    # 示例转换为 uint8 类型
    print("Converting data to uint8")
    data = data.astype(np.uint8)
    print(f"Converted data type: {data.dtype}")

transform = dataset.GetGeoTransform()
affine_transform = from_origin(transform[0], transform[3], transform[1], transform[5])

# 设定草地区域的值（根据实际情况）
grassland_value = 10

# 创建掩模，将草地区域提取出来
mask_array = np.where(data == grassland_value, 1, 0)

# 确保掩模数组的数据类型符合要求
mask_array = mask_array.astype(np.uint8)  # 确保数据类型为 uint8

# 使用 rasterio.features.shapes 生成 GeoJSON 形状
shapes_gen = rasterio.features.shapes(mask_array, transform=affine_transform)

# 检查生成的形状
geoms = []
values = []
for feature in shapes_gen:
    geoms.append(shape(feature[0]))
    values.append(feature[1])

# 打印长度以确认
print(f"Length of geoms: {len(geoms)}")
print(f"Length of values: {len(values)}")

# 确保 geoms 和 values 长度一致
if len(geoms) != len(values):
    raise ValueError("Length of geoms and values does not match!")

# 创建 GeoDataFrame
gdf = gpd.GeoDataFrame({'geometry': geoms, 'value': values})

# 计算每个草地区域的面积
gdf['area'] = gdf.geometry.area

print(gdf[gdf['area'] > 1000])

# # 过滤出大于某个阈值的区域（可选）
# threshold = 100000  # 10,000,000 平方米（10 平方公里）
# large_grasslands = gdf[gdf['area'] > threshold]

# # 打印每个草地区域的面积
# for _, row in large_grasslands.iterrows():
#     print(f"Feature Area: {row['area']} sqm")

# 保存到文件（可选）
# output_file = '/path/to/save/large_grasslands.geojson'
# large_grasslands.to_file(output_file, driver='GeoJSON')
