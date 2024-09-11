from osgeo import gdal
import rasterio
import geopandas as gpd
from rasterio.mask import mask
from rasterio.features import shapes as rasterio_shapes
import json
import os

# 确保使用绝对路径
hdf_file = '/home/r/Desktop/r-climate/data/MCD12C1.A2020001.061.2022172062638.hdf'
geojson_file = '/home/r/Desktop/r-climate/geojson/polygon_geojson.geojson'
tiff_file = '/home/r/Desktop/r-climate/data/temp.tif'

# 读取 HDF 文件中的图层，替换 'GridName' 为实际的图层名称
subdataset_name = 'HDF4_EOS:EOS_GRID:"{}":MOD12C1:Majority_Land_Cover_Type_1'.format(hdf_file)
dataset = gdal.Open(subdataset_name)
gdal.Translate(tiff_file, dataset)

# 读取 GeoJSON 文件
gdf = gpd.read_file(geojson_file)

# 使用 Rasterio 打开转换后的 TIFF 文件
with rasterio.open(tiff_file) as src:
    geojson_shapes = [feature['geometry'] for feature in gdf.iterfeatures()]
    out_image, out_transform = mask(src, geojson_shapes, crop=True)

    out_meta = src.meta.copy()
    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    # 保存裁剪后的数据为新的 TIFF 文件
    clipped_tiff = '/home/r/Desktop/r-climate/data/clipped_data.tif'
    with rasterio.open(clipped_tiff, 'w', **out_meta) as dest:
        dest.write(out_image)

# 将裁剪后的 TIFF 文件转换为 GeoJSON
with rasterio.open(clipped_tiff) as src:
    image = src.read(1)
    mask_data = image != src.nodata  # 更改变量名以避免覆盖内置函数
    result_shapes = list(rasterio_shapes(image, mask=mask_data, transform=src.transform))  # 使用不同的变量名

    features = []
    for geom, value in result_shapes:
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {"value": value}
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

# 保存为 GeoJSON 文件
output_geojson = '/home/r/Desktop/r-climate/data/clipped_data.geojson'
with open(output_geojson, 'w') as f:
    json.dump(geojson, f)

# 删除临时文件
os.remove(tiff_file)
