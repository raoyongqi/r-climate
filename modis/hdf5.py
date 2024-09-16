from osgeo import gdal

# HDF 文件路径
file_path = '/home/r/Desktop/r-climate/data/MCD12C1.A2020001.061.2022172062638.hdf'

# 打开 HDF 文件
dataset = gdal.Open(file_path, gdal.GA_ReadOnly)

# 打印所有子数据集的信息
if dataset is not None:
    print("文件打开成功!")
    for i in range(dataset.RasterCount):
        band = dataset.GetRasterBand(i + 1)
        print(f"Band {i + 1}:")
        print(f"  Data type: {gdal.GetDataTypeName(band.DataType)}")
        print(f"  Size: {band.XSize} x {band.YSize}")
else:
    print("文件打开失败!")

# 关闭数据集
dataset = None
