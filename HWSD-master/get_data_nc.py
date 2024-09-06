#数据分布规则，直接使用索引

import pandas as pd
import numpy as np
import os
import xarray as xr
from concurrent.futures import ThreadPoolExecutor

# 输入文件路径和文件夹路径
excel_file = 'data/final_data.xlsx'
nc_folder = 'HWSD_1247/data'
output_excel = 'data/output_data.xlsx'

# 读取 Excel 文件中的经纬度数据
df = pd.read_excel(excel_file)

# 确保 DataFrame 中存在 LAT 和 LON 列
if 'LAT' not in df.columns or 'LON' not in df.columns:
    raise ValueError("Excel file must contain 'LAT' and 'LON' columns")

# 定义一个函数来从 NetCDF 文件中获取波段数据
def get_band_data(nc_file, lat_lon_points):
    with xr.open_dataset(nc_file) as ds:
        latitudes = ds['lat'].values
        longitudes = ds['lon'].values

        # 使用 numpy 来找到最近的经纬度索引
        lat_idx = np.abs(latitudes[:, np.newaxis] - lat_lon_points[:, 1]).argmin(axis=0)
        lon_idx = np.abs(longitudes[:, np.newaxis] - lat_lon_points[:, 0]).argmin(axis=0)
        
        band_data = {}
        for band_name in ds.data_vars:
            if band_name in ['lat', 'lon']:
                continue
            
            # 直接使用索引来提取最近的波段数据
            band_values = ds[band_name].values
            closest_band_data = band_values[lat_idx, lon_idx]
            band_data[band_name] = np.where(np.isnan(closest_band_data), -9999, closest_band_data)
        
        return band_data

# 获取文件夹中的所有 NetCDF 文件
nc_files = [f for f in os.listdir(nc_folder) if f.endswith('.nc') or f.endswith('.nc4')]

lat_lon_points = df[['LON', 'LAT']].values

# 并行处理 NetCDF 文件
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_band_data, os.path.join(nc_folder, nc_file), lat_lon_points): nc_file for nc_file in nc_files}
    for future in futures:
        band_data = future.result()
        for band_name, values in band_data.items():
            df[band_name] = values

# 将结果输出为新的 Excel 文件
df.to_excel(output_excel, index=False)
print(f'Results have been saved to {output_excel}')
