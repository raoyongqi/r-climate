# 检查对象是否存在
if (!exists("result")) {
  # 如果对象不存在，则从Excel文件中读取数据
  # 需要先安装并加载readxl包
  if (!require(readxl)) install.packages("readxl", dependencies = TRUE)
  library(readxl)
  
  # 从Excel文件中读取数据
  result <- read_excel("climate_data.xlsx")
}

site_data <- read_excel("1_Alldata.xlsx", sheet = "Plotdata")

names(result) <- ifelse(
  tolower(names(result)) %in% c("lon", "lat"),
  toupper(names(result)),
  names(result)
)
if (!require(dplyr)) install.packages("dplyr")
library(dplyr)
merged_df <- site_data %>%
  left_join(result, by = "site")

output_file_path <- "final_data.xlsx"

write.xlsx(merged_df, output_file_path, rowNames = FALSE)

# 完成
cat("气候数据已成功保存到", output_file_path, "\n")


