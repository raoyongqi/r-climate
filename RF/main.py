import squarify
import matplotlib.pyplot as plt
import pandas as pd
import re

# 读取数据
df = pd.read_csv("data/model/feature_importances.csv")

# 去除 'wc2.1_5m_' 前缀
df["Feature"] = df["Feature"].str.replace('^wc2.1_5m_', '', regex=True)

# 处理重复的下划线内容
def simplify_feature_name(name):
    # 用正则表达式去除下划线两边相同的内容
    return re.sub(r'(_\w+)\1', r'\1', name)

df["Feature"] = df["Feature"].apply(simplify_feature_name)

# 创建图形
fig, ax = plt.subplots(figsize=(12, 10))  # 增大图形尺寸
ax.set_axis_off()

# 定义颜色映射
color_mapping = {
    "geo": "green",   # geo 映射成绿色
    "soil": "blue",   # soil 映射成蓝色
    "clim": "orange"  # clim 映射成橙色
}

# 确保 'Category' 列在 DataFrame 中
df["Category"] = df["Feature"].apply(lambda x: next((key for key in color_mapping if key in x), "unknown"))

# 根据 Category 列映射颜色，并处理 NaN 值
colors = df["Category"].map(color_mapping).fillna('gray')

# 绘制树形图
squarify.plot(
    sizes=df["Importance"],
    label=df["Feature"],
    color=colors,
    alpha=.7,
    ax=ax
)

# 创建图例
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_mapping[cat], markersize=10) for cat in color_mapping]
plt.legend(handles, color_mapping.keys(), title="Features", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', title_fontsize='13')

# 调整布局
plt.subplots_adjust(right=0.8)  # 调整右边的边距，以确保图例不会被截断

# 保存图像
plt.savefig('data/model/feature_importance_treemap.png', bbox_inches='tight')  # 保存图像
# plt.show()  # 显示图像
