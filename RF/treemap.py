import squarify
import matplotlib.pyplot as plt
import pandas as pd
import squarify # pip install squarify (algorithm for treemap)
import matplotlib.pyplot as plt
from pypalettes import load_cmap
import pandas as pd
from highlight_text import fig_text
# 设置更高的分辨率
plt.rcParams['figure.dpi'] = 300

# 读取数据
df = pd.read_csv("https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/simple-treemap.csv")

# 创建图形
cmap = load_cmap('Acadia')
category_codes, unique_categories = pd.factorize(df['parent'])
colors = [cmap(code) for code in category_codes]

# create a treemap
fig, ax = plt.subplots(figsize=(10,10))
ax.set_axis_off()
squarify.plot(
   sizes=df["value"],
   label=df["name"],
   color=colors,
   text_kwargs={'color':'white'},
   pad=True,
   ax=ax
)

# 保存图像
plt.savefig('data/model/feature_importance_treemap.png')  # 保存图像