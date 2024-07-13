install.packages("raster")
install.packages("sp")
install.packages("terra")
library(raster)
options(timeout = 3000)

install.packages("terra")
setwd("C:/Users/r/Desktop/r_climate/data")
library(openxlsx)
data <- read.xlsx("lat_lon.xlsx", sheet = 1)
names(data) <- tolower(names(data))


if(!all(c('lon', 'lat') %in% names(data))) {
  stop("Excel 文件需要包含 'lon' 和 'lat' 列")
}



variables <- c('bio', 'tmin', 'tmax', 'prec')

# 定义一个函数来下载和提取单个样点的数据
download_and_extract <- function(lon, lat, var, res = 0.5) {
  clim_data <- getData('worldclim', var = var, res = res, lon = lon, lat = lat)
  return(extract(clim_data, matrix(c(lon, lat), ncol = 2)))
}
worldclim <- raster::getData('worldclim', var='prec', res=2.5, lon = 142.61, lat = -23.64)

# 迭代每个样点，下载并提取数据
for (var in variables) {
  all_clim_values <- NULL
  
  for (i in 1:nrow(points)) {
    lon <- points$x[i]
    lat <- points$y[i]
    
    clim_values <- download_and_extract(lon, lat, var)
    
    if (is.null(all_clim_values)) {
      all_clim_values <- clim_values
    } else {
      all_clim_values <- rbind(all_clim_values, clim_values)
    }
  }
  
  # 给提取到的数据添加前缀
  colnames(all_clim_values) <- paste(var, colnames(all_clim_values), sep = "_")
  
  # 将提取到的数据与原始样点数据合并
  result <- cbind(result, all_clim_values)
}

# 保存结果到新的 Excel 文件
output_file_path <- "climate_data.xlsx"
write_xlsx(result, output_file_path)