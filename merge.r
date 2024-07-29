# 示例数据框 df1
# 加载必要的包
library(openxlsx)
  # 添加对 utils 包的引用

# 设置工作目录
setwd("C:/Users/r/Desktop/r_climate/data")

# 读取 Excel 文件中的经纬度数据
data <- read.csv("Plotdata.csv")
# 添加行号列
library(dplyr)
result <- read.xlsx("climate_data.xlsx")
site_data <- read.csv("Lacation.csv")


names(result) <- ifelse(
  tolower(names(result)) %in% c("lon", "lat"),
  toupper(names(result)),
  names(result)
)

merged_df <- site_data %>%
  left_join(result, by = c("LAT", "LON"))

merged_df <- merged_df %>%
  left_join(data, by = "Site")


output_file_path <- "final_data.xlsx"
write.xlsx(merged_df, output_file_path, rowNames = FALSE)

# 完成
cat("气候数据已成功保存到", output_file_path, "\n")
