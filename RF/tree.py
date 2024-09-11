import squarify
import matplotlib.pyplot as plt
import pandas as pd

# 设置更高的分辨率
plt.rcParams['figure.dpi'] = 300

# 读取数据
df = pd.read_csv("https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/simple-treemap.csv")

# 创建图形
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_axis_off()

# 绘制树形图
squarify.plot(
   sizes=df["value"],
   label=df["name"],
   ax=ax
)

# 保存图像
plt.savefig('data/model/feature_importance_treemap.png')  # 保存图像
