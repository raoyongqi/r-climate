import rasterio

def print_tiff_projection(file_path):
    with rasterio.open(file_path) as src:
        # 打印投影信息
        print("Projection Information:")
        print(src.crs)  # Coordinate Reference System (CRS)
        print("Affine Transformation:")
        print(src.transform)  # Affine transformation
        print("Metadata:")
        print(src.meta)  # 元数据

# 替换为你的 TIFF 文件路径
print_tiff_projection(    '/home/r/Desktop/r-climate/data/HWSD_1247/tif/AWT_T_SOC_SUM_t_c_12_resampled.tif')
