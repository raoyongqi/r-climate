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
result_with_row_num <- result %>%
  mutate(Site = row_number())
merged_df <- data %>%
  left_join(result_with_row_num, by = "Site")
