import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 创建示例相关性矩阵
correlation_coef = np.array([[1, -0.17, 0.04],
                              [-0.17, 1, -0.05],
                              [0.04, -0.05, 1]])
# 设置行和列的名称
rows = ['cg225', 'cg271', 'cg215']
cols = ['cg225', 'cg271', 'cg215']

# 创建 DataFrame
corr_df = pd.DataFrame(correlation_coef, index=rows, columns=cols)

# 提取上三角部分（不包括对角线）
ut = np.triu(np.ones(corr_df.shape), k=1).astype(bool)

# 创建新 DataFrame，包含上三角部分的数据
utdf = pd.DataFrame({
    'row': corr_df.index.values[np.where(ut)[0]],
    'col': corr_df.columns.values[np.where(ut)[1]],
    'corr': corr_df.values[ut]
})

# 创建一个透视表，适应热图的格式
heatmap_data = utdf.pivot(index='row', columns='col', values='corr')

# 过滤掉全为 NaN 的行和列
heatmap_data = heatmap_data.dropna(how='all', axis=0).dropna(how='all', axis=1)

# 绘制热图
plt.figure(figsize=(8, 6))
plt.imshow(heatmap_data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

# 添加颜色条
plt.colorbar(label='Correlation Coefficient')

# 显示数值
for (i, j), val in np.ndenumerate(heatmap_data):
    plt.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')

# 设置刻度
plt.xticks(ticks=np.arange(len(heatmap_data.columns)), labels=heatmap_data.columns, rotation=45)
plt.yticks(ticks=np.arange(len(heatmap_data.index)), labels=heatmap_data.index)

# 显示热图
plt.show()
