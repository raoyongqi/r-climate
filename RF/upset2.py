import pandas as pd
from upsetplot import UpSet
import matplotlib.pyplot as plt

# 读取并合并所有特征重要性 CSV 文件
def generate_upset_df(importance_csv_files):
    all_data = []
    for csv_file in importance_csv_files:
        df = pd.read_csv(csv_file)
        df['Source'] = csv_file.split('/')[-1].replace('.csv', '')  # 用文件名作为源
        all_data.append(df)
    return pd.concat(all_data)

# 获取 UpSet 图所需的数据
importance_csv_files = [
    'data/model/feature_importances_geo.csv',
    'data/model/feature_importances_clim_geo.csv',
    'data/model/feature_importances_all.csv'
]

upset_df = generate_upset_df(importance_csv_files)

# 将数据转换为布尔型的集合
def prepare_upset_data(df):
    # 创建布尔索引 DataFrame
    boolean_df = pd.DataFrame()

    # 处理每个类别（geo, clim, soil）
    for category in ['geo', 'clim', 'soil']:
        category_df = df[df['Category'] == category]
        category_boolean = pd.get_dummies(category_df['Feature'])
        
        # 确保索引唯一
        category_boolean = category_boolean.groupby(category_boolean.index).max()
        category_boolean['Count'] = category_df['Importance']
        
        # 合并时防止重复索引
        category_boolean.reset_index(drop=True, inplace=True)
        boolean_df = pd.concat([boolean_df, category_boolean], axis=1, sort=False)

    # 对所有特征进行布尔编码
    boolean_df = boolean_df.groupby(boolean_df.index).sum()
    boolean_df = boolean_df.astype(bool)
    
    # 计算每个布尔组合的计数
    upset_data = boolean_df.groupby(list(boolean_df.columns)).size()
    
    return upset_data

# 处理数据并生成 UpSet 图
upset_data = prepare_upset_data(upset_df)

# 生成 UpSet 图
upset_plot = UpSet(upset_data)
upset_plot.plot()
plt.suptitle("Feature Importance UpSet Plot")
plt.show()
