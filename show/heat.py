import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取 Excel 文件
df = pd.read_excel('data/output_data.xlsx')

# 设置行和列的名称
rows = ['LON', 'wc2.1_5m_srad_04', 'wc2.1_5m_srad_07', 'wc2.1_5m_srad_02']
cols = ['LON', 'wc2.1_5m_srad_04', 'wc2.1_5m_srad_07', 'wc2.1_5m_srad_02']

# 选择特定的列
columns_to_select = rows
df_selected = df[columns_to_select]

# 计算相关系数矩阵
corr_matrix = df_selected.corr()

# 创建掩码，只显示下三角部分
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=0)  # k=0 包括对角线

# 提取下三角部分的相关系数（不包括对角线）
lower_triangle_corr = corr_matrix.where(~mask)

# 过滤掉全为 NaN 的行和列
heatmap_data = lower_triangle_corr.dropna(how='all', axis=0).dropna(how='all', axis=1)

# 绘制热图
plt.figure(figsize=(8, 6))
plt.imshow(heatmap_data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

# 添加颜色条
plt.colorbar(label='Correlation Coefficient')

# 显示数值
for (i, j), val in np.ndenumerate(heatmap_data):
    if not np.isnan(val):  # 只在有值的地方显示
        plt.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')

# 设置刻度
plt.xticks(ticks=np.arange(len(heatmap_data.columns)), labels=heatmap_data.columns, rotation=45)
plt.yticks(ticks=np.arange(len(heatmap_data.index)), labels=heatmap_data.index)

# 设置标题
plt.title('Correlation Matrix of Selected Variables (Lower Triangle Only)')


title ='Correlation Matrix of Selected Variables (Including Diagonal)'
# 设置标题
output_file_path = f'data/{title}.png'
plt.savefig(output_file_path, dpi=300, bbox_inches='tight')

# 显示热图
# 显示热图
plt.tight_layout()  # 调整布局
plt.show()
