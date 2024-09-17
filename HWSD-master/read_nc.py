import xarray as xr
# nc_file = Dataset()

# 打开 NetCDF 文件
ds = xr.open_dataset('/home/r/Desktop/r-climate/data/HWSD_1247/data/AWC_CLASS.nc4')

# 获取 CRS 信息
crs = ds.attrs  # 这里的 'crs' 是 CRS 属性的名称，具体名称可能有所不同
print(crs)

# 关闭数据集
ds.close()
