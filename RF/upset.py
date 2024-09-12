import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import matplotlib.pyplot as plt
from upsetplot import UpSet

# 1. 读取 Excel 文件
file_path = 'data/output_data.xlsx'  # 替换为你的文件路径
data = pd.read_excel(file_path)

# 2. 定义特征选择函数
def train_model(data, feature_columns, model_save_path, importance_save_path):
    X = data[feature_columns]
    y = data['PL']  # 目标变量
    
    # 分割数据集为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 初始化并训练随机森林回归模型
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # 预测并评估模型
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"均方误差 (MSE): {mse:.4f}")
    print(f"R² 得分: {r2:.4f}")

    # 保存模型
    joblib.dump(rf, model_save_path)

    # 保存变量重要性
    feature_importances = rf.feature_importances_
    data = []
    for feature_name, importance_value in zip(feature_columns, feature_importances):
        # 根据特征列判断类别
        if feature_name.lower() in ["lon", "lat"]:
            category = "geo"
        elif feature_name.startswith('wc'):
            category = "clim"
        else:
            category = "soil"

        data.append({
            "Feature": feature_name,
            "Importance": importance_value,
            "Category": category
        })

    importance_df = pd.DataFrame(data)
    importance_df.sort_values(by='Importance', ascending=False).to_csv(importance_save_path, index=False)

# 3. 定义特征组合
feature_combinations = {
    'geo': ['LON', 'LAT'],
    'clim_geo': [col for col in data.columns if col.lower().startswith('wc')] + ['LON', 'LAT'],
    'all': [col for col in data.columns if col.endswith('_resampled') or col.lower().startswith('wc') or col in ['LON', 'LAT']]
}

# 4. 训练模型并保存变量重要性
os.makedirs('data/model', exist_ok=True)

for key, features in feature_combinations.items():
    model_path = f'data/model/random_forest_model_{key}.pkl'
    importance_path = f'data/model/feature_importances_{key}.csv'
    train_model(data, features, model_path, importance_path)

# 5. 生成 UpSet 图
def generate_upset_df(importance_csv_files):
    all_data = []
    for csv_file in importance_csv_files:
        df = pd.read_csv(csv_file)
        df['Source'] = csv_file.split('/')[-1].replace('.csv', '')  # 用文件名作为源
        all_data.append(df)
    return pd.concat(all_data)

importance_csv_files = [
    'data/model/feature_importances_geo.csv',
    'data/model/feature_importances_clim_geo.csv',
    'data/model/feature_importances_all.csv'
]

# 生成 UpSet 数据
upset_df = generate_upset_df(importance_csv_files)
print(upset_df)