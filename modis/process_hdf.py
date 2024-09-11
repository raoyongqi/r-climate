from osgeo import gdal

import rasterio
import geopandas as gpd
from rasterio.mask import mask
from rasterio.features import shapes
import json

# 打开 HDF 文件
hdf_file = 'MCD12C1.A2020001.061.2022172062638.hdf'
dataset = gdal.Open(f'HDF4_EOS:EOS_GRID:{hdf_file}:"GridName"')

# 读取 GeoJSON 文件
geojson_file = 'geojson/polygon_geojson.geojson'
gdf = gpd.read_file(geojson_file)

# 获取 HDF 文件中的栅格图层
raster_layer = 'GridName'  # 替换为实际的层名称

# 保存 HDF 图层为 TIFF 文件
with rasterio.open(f'HDF4_EOS:EOS_GRID:{hdf_file}:"{raster_layer}"') as src:
    # GeoJSON 转换为掩膜
    shapes = [feature['geometry'] for feature in gdf.iterfeatures()]
    out_image, out_transform = mask(src, shapes, crop=True)

    # 更新 metadata
    out_meta = src.meta.copy()
    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    # 保存裁剪后的数据
    with rasterio.open('clipped_data.tif', 'w', **out_meta) as dest:
        dest.write(out_image)

# 转换为 GeoJSON
with rasterio.open('clipped_data.tif') as src:
    image = src.read(1)
    mask = image != src.nodata
    results = list(shapes(image, mask=mask, transform=src.transform))

    features = []
    for geom, value in results:
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
with open('clipped_data.geojson', 'w') as f:
    json.dump(geojson, f)
