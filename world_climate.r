remotes::install_github("brunomioto/WorldClimData")
download_worldclim_data <- function(variables, period = "current", resolution = 10, folder_path = "./WorldClim_data") {
  for (variable in variables) {
    download_worldclim(
      period = period,
      variable = variable,
      resolution = resolution,
      folder_path = folder_path
    )
  }
}
library(WorldClimData)
# 定义要下载的变量
variables <- c("bio", "elev", "prec", "srad", "tavg", "tmax", "tmin", "vapr", "wind")

# 调用函数下载所有变量的数据
download_worldclim_data(variables, period = "current", resolution = 10, folder_path = "./WorldClim_data")
