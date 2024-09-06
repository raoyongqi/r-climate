import xarray as xr
import rasterio
from rasterio.transform import from_origin
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject
import os

# 输入和输出文件夹路径
input_folder = 'HWSD_1247/data'
output_folder = 'TIF'

# 目标分辨率（5 分钟）
target_resolution = 0.083333  # 5 minutes

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的 NetCDF 文件
for file_name in os.listdir(input_folder):
    if file_name.endswith('.nc4'):
        # 构建完整的输入和输出文件路径
        input_file = os.path.join(input_folder, file_name)
        output_file = os.path.join(output_folder, f'{os.path.splitext(file_name)[0]}.tif')
        
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
            'transform': transform
        }
        
        # 写入初始分辨率的 GeoTIFF 文件
        temp_file = 'temp.tif'
        with rasterio.open(temp_file, 'w', **meta) as dst:
            dst.write(data, 1)

        # 重采样到目标分辨率
        with rasterio.open(temp_file) as src:
            transform, width, height = calculate_default_transform(
                src.crs, src.crs, src.width, src.height,
                src.bounds.left, src.bounds.bottom,
                src.bounds.right, src.bounds.top,
                resolution=(target_resolution, target_resolution)
            )
            
            kwargs = src.meta.copy()
            kwargs.update({
                'transform': transform,
                'width': width,
                'height': height
            })
            
            with rasterio.open(output_file, 'w', **kwargs) as dst:
                reproject(
                    source=rasterio.band(src, 1),
                    destination=rasterio.band(dst, 1),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=src.crs,
                    resampling=Resampling.bilinear
                )

        # 删除临时文件
        os.remove(temp_file)

        print(f'Converted {input_file} to {output_file}')
