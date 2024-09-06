import xarray as xr

# 打开 NetCDF 文件
input_file = 'HWSD_1247/data/AWC_CLASS.nc4'  # 具体的 NetCDF 文件路径
ds = xr.open_dataset(input_file)

# 打印所有变量的名字
# print("Variables in NetCDF file:")
print(ds.variables[list(ds.variables.keys())[2]])

# 打印 NetCDF 文件的基本信息
# print(ds)

# # 打印每个变量的详细信息，包括维度和数据类型
# for var in ds.data_vars:
#     print(f"\nVariable: {var}")
    # print(ds[var])
    # print("Data shape:", ds[var].shape)
    # print("Data type:", ds[var].dtype)
    # print("Data range:", ds[var].min().values, "to", ds[var].max().values)
