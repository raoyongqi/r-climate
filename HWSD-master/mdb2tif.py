import pandas as pd
from sqlalchemy import create_engine
import rasterio
from rasterio.transform import from_origin
import numpy as np

# 数据库连接字符串
mdb_file =  'HWSD/HWSD.mdb'
conn_str = f'mssql+pyodbc:///?odbc_connect=DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={mdb_file};'

# 创建数据库引擎
engine = create_engine(conn_str)

# 读取数据到 DataFrame
query = "SELECT * FROM your_table_name"
df = pd.read_sql(query, engine)

# 假设 DataFrame 中有 'x', 'y' 和 'value' 列
x = df['x'].values
y = df['y'].values
values = df['value'].values

# 定义栅格大小
pixel_size = 1
width = int((x.max() - x.min()) / pixel_size)
height = int((y.max() - y.min()) / pixel_size)

# 创建空的栅格数组
raster = np.full((height, width), np.nan)

# 填充栅格数组
for i in range(len(values)):
    row = int((y.max() - y[i]) / pixel_size)
    col = int((x[i] - x.min()) / pixel_size)
    raster[row, col] = values[i]

# 定义仿射变换
transform = from_origin(x.min(), y.max(), pixel_size, pixel_size)

# 保存为 TIFF 文件
with rasterio.open(
    'output_image.tif', 'w',
    driver='GTiff',
    height=raster.shape[0],
    width=raster.shape[1],
    count=1,
    dtype=raster.dtype,
    crs='+proj=latlong',
    transform=transform,
) as dst:
    dst.write(raster, 1)

print("TIFF image created and saved as 'output_image.tif'")
