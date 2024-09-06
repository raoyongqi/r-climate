import xarray as xr
import rasterio
from rasterio.transform import from_origin
import numpy as np
import os

# 输入和输出文件路径
input_file = 'HWSD_1247/data/AWC_CLASS.nc4'   # 具体的 NetCDF 文件路径
output_file = 'TIF/your_file.tif'  # 输出的 GeoTIFF 文件路径

# 创建输出文件夹（如果不存在）
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# 打开 NetCDF 文件
ds = xr.open_dataset(input_file)

# 选择第一个变量进行转换
variable = list(ds.data_vars.keys())[0]  # 默认选择第一个变量
data = ds[variable].values

# 处理多维数据
if len(data.shape) > 2:
    # 假设我们选择第一个时间步长或第一个层次
    data = data[0]  # 修改此处根据实际数据选择

# 获取坐标信息
lat = ds['lat'].values
lon = ds['lon'].values

# 原始分辨率
orig_resolution_x = lon[1] - lon[0]
orig_resolution_y = lat[1] - lat[0]

# 计算变换
transform = from_origin(lon.min(), lat.max(), orig_resolution_x, orig_resolution_y)

# 更新元数据
meta = {
    'driver': 'GTiff',
    'count': 1,
    'dtype': 'float32',
    'width': len(lon),
    'height': len(lat),
    'crs': 'EPSG:4326',  # 根据实际坐标系调整
    'transform': transform,
    'nodata': -9999  # 指定一个 nodata 值
}

# 替换 NaN 或无效值
data = np.where(np.isnan(data), -9999, data)

# 写入 GeoTIFF 文件
with rasterio.open(output_file, 'w', **meta) as dst:
    dst.write(data, 1)

print(f'Converted {input_file} to {output_file}')
