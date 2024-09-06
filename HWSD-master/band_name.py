import rasterio

# 打开 TIFF 文件
tif_file = "HWSD_RASTER/hwsd.tif"

with rasterio.open(tif_file) as src:
    # 打印总波段数
    num_bands = src.count
    print(f"Number of bands: {num_bands}")

    # 访问和打印每个波段的元数据
    for i in range(1, num_bands + 1):
        band_tags = src.tags(i)
        print(f"Band {i}:")
        print(f"  Metadata: {band_tags}")

        # 如果波段名称存在于元数据中，通常可以找到类似 'description' 或 'name' 的键
        if 'description' in band_tags:
            print(f"  Description: {band_tags['description']}")
        else:
            print(f"  Description: Not available")
