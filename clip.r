library(raster)
library(rgdal)
library(sf)
# install.packages("rgdal")
# install.packages("sf")
# 读取GeoJSON文件
setwd("C:/Users/r/Desktop/r_climate/data")

geojson_path <- "geojson/Pan.geojson"
geojson <- st_read(geojson_path)

# 读取TIF文件
tif_path <- "climate/wc2.1_10m/wc2.1_10m_bio_1.tif"
tif <- raster(tif_path)

# 根据GeoJSON剪切TIF
cropped_tif <- crop(tif, geojson)

# 掩膜处理，去掉不在剪切范围内的区域
masked_tif <- mask(cropped_tif, geojson)

# 保存剪切后的TIF文件
output_path <- "clipped/file_cropped.tif"
writeRaster(masked_tif, filename = output_path, format = "GTiff", overwrite = TRUE)

# 返回剪切后的TIF文件路径
output_path
plot(masked_tif)
