import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 读取 Excel 文件
df = pd.read_excel('data/output_data.xlsx')

# 选择特定的列
columns_to_select = [
    'wc2.1_5m_srad_10',
    'LON',
    'wc2.1_5m_srad_04',
    'wc2.1_5m_srad_07',
    'wc2.1_5m_srad_02',
]
df_selected = df[columns_to_select]

# 计算相关系数矩阵
corr_matrix = df_selected.corr()

# 创建掩码，只显示对角线以下部分
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# 将对角线元素设为 NaN
np.fill_diagonal(corr_matrix.values, np.nan)

# 设置绘图风格
sns.set(style='white')

# 绘制热图
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', mask=mask, square=True, cbar_kws={"shrink": .8}, vmin=-1, vmax=1)
plt.title('Correlation Matrix of Selected Variables (Lower Triangle without Diagonal)')
plt.show()
