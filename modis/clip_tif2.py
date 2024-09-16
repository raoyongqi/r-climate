import os
import rasterio
from rasterio.mask import mask
import numpy as np
import geopandas as gpd

# 1. 加载 GeoJSON 文件
grasslands_geojson_file = '/home/r/Desktop/r-climate/data/clipped_data.geojson'
grasslands_gdf = gpd.read_file(grasslands_geojson_file)

# 2. 筛选出值等于 10 的 Grasslands (草地)
grasslands_gdf_filtered = grasslands_gdf[grasslands_gdf['value'] == 10]

# 输入文件夹列表
tiff_folders = [
    '/home/r/Desktop/r-climate/data/climate/wc2.1_5m/',
    '/home/r/Desktop/r-climate/data/climate/other_folder/'
]

# 指定输出文件夹路径
geojson_output_folder = '/home/r/Desktop/r-climate/cropped_data/geojson/'
tiff_output_folder = '/home/r/Desktop/r-climate/cropped_data/tiff/'

# 创建输出文件夹（如果不存在）
os.makedirs(geojson_output_folder, exist_ok=True)
os.makedirs(tiff_output_folder, exist_ok=True)

# 使用 GeoDataFrame 中的 'geometry' 列直接作为几何对象
geometries = grasslands_gdf_filtered['geometry']

# 遍历 TIFF 文件夹列表中的每个文件夹
for tiff_folder in tiff_folders:
    for tiff_file in os.listdir(tiff_folder):
        if tiff_file.endswith('.tif'):
            tiff_path = os.path.join(tiff_folder, tiff_file)
            
            # 构建输出路径
            tiff_output_path = os.path.join(tiff_output_folder, f'cropped_{tiff_file}')
            geojson_output_path = os.path.join(geojson_output_folder, f'cropped_{os.path.splitext(tiff_file)[0]}.geojson')

            # 读取 TIFF 文件
            with rasterio.open(tiff_path) as src:
                # 读取所有波段并转换为浮点型
                image_data = src.read().astype(np.float32)

                # 创建一个临时的内存文件来保存转换后的图像
                with rasterio.MemoryFile() as memfile:
                    with memfile.open(
                        driver="GTiff",
                        height=image_data.shape[1],
                        width=image_data.shape[2],
                        count=image_data.shape[0],
                        dtype="float32",
                        crs=src.crs,
                        transform=src.transform,
                        nodata=np.nan,
                    ) as dataset:
                        dataset.write(image_data)

                        # 使用 GeoDataFrame 的几何对象进行剪切，并处理缺失值
                        out_image, out_transform = mask(dataset, geometries, crop=True, nodata=np.nan)

                        # 更新元数据
                        out_meta = dataset.meta.copy()
                        out_meta.update({
                            "driver": "GTiff",
                            "height": out_image.shape[1],
                            "width": out_image.shape[2],
                            "transform": out_transform,
                            "dtype": "float32",  # 保持数据类型为浮点型
                            "nodata": np.nan
                        })

                        # 保存剪切后的 TIFF 结果
                        with rasterio.open(tiff_output_path, "w", **out_meta) as dest:
                            dest.write(out_image)

            # 为每个 TIFF 文件保存一个对应的 GeoJSON 文件
            grasslands_gdf_filtered.to_file(geojson_output_path, driver="GeoJSON")
            
            print(f"Clipped TIFF image saved to {tiff_output_path}")
            print(f"Corresponding GeoJSON saved to {geojson_output_path}")
