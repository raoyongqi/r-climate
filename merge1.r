# 检查对象是否存在
if (!require(dplyr)) install.packages("dplyr")
library(dplyr)
library(openxlsx)
sys_info <- Sys.info()
if (!is.null(sys_info)) {
  if (sys_info['sysname'] == 'Windows') {
    print("系统是Windows")
    setwd("C:/Users/r/Desktop/rclimate/data")
    
  } else if (sys_info['sysname'] == 'Linux') {
    os_release <- readLines('/etc/os-release')
    if (any(grepl("Ubuntu", os_release))) {
      print("系统是Ubuntu")
      setwd("~/Desktop/getData/rclimate/data")
      
      
    } else {
      print("系统是其他Linux发行版")
    }
  } else {
    print("系统不是Windows或Ubuntu")
  }
} else {
  print("无法获取系统信息")
}




if (!exists("result")) {
  # 如果对象不存在，则从Excel文件中读取数据
  # 需要先安装并加载readxl包
  if (!require(readxl)) install.packages("readxl", dependencies = TRUE)
  library(readxl)
  
  # 从Excel文件中读取数据
  result <- read_excel("climate_data.xlsx")
}

site_data <- read_excel("1_Alldata.xlsx", sheet = "Plotdata")
# 去掉 'site' 列（如果存在）
if ("site" %in% names(site_data)) {
  site_data <- site_data %>%
    select(-site)
}

# 将 'Site' 列重命名为 'site'（如果存在）
if ("Site" %in% names(site_data)) {
  site_data <- site_data %>%
    rename(site = Site)
}
names(result) <- ifelse(
  tolower(names(result)) %in% c("lon", "lat"),
  toupper(names(result)),
  names(result)
)

merged_df <- site_data %>%
  left_join(result, by = "site")

output_file_path <- "final_data.xlsx"

write.xlsx(merged_df, output_file_path, rowNames = FALSE)

# 完成
cat("气候数据已成功保存到", output_file_path, "\n")


