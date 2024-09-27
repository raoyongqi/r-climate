import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import SelectFromModel
import joblib  # 用于保存模型
import os  # 用于处理文件和目录

# 1. 读取Excel文件
file_path = 'data/output_data.xlsx'  # 替换为你的文件路径
data = pd.read_excel(file_path)

# 2. 筛选特征列：以 '_resampled' 结尾，'wc' 开头（不区分大小写），以及 'LON' 和 'LAT' 列
feature_columns = [col for col in data.columns if col.endswith('_resampled') or col.lower().startswith('wc') or col in ['LON', 'LAT']]

# 3. 分离特征变量和目标变量
X = data[feature_columns]
y = data['PL']  # 目标变量

# 4. 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 初始化并训练随机森林回归模型
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 6. 特征选择
selector = SelectFromModel(rf, threshold="mean", prefit=True)
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

# 7. 训练基于选择特征的模型
rf_selected = RandomForestRegressor(n_estimators=100, random_state=42)
rf_selected.fit(X_train_selected, y_train)

# 8. 预测并评估模型
y_pred = rf_selected.predict(X_test_selected)

# 9. 评估模型性能
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 输出结果
print(f"均方误差 (MSE): {mse:.4f}")
print(f"R² 得分: {r2:.4f}")

# 10. 确保保存路径存在
os.makedirs('data/model', exist_ok=True)

# 11. 保存模型
joblib.dump(rf_selected, 'data/model/random_forest_model.pkl')

# 12. 保存变量重要性
feature_importances = rf_selected.feature_importances_

# 遍历特征列和特征重要性
import re
data = []

# 使用选择后的特征
selected_features = [feature for feature, selected in zip(feature_columns, selector.get_support()) if selected]

for feature_name, importance_value in zip(selected_features, feature_importances):
    feature_name = re.sub('_resampled', '', feature_name)  # 移除 '_resampled'
    
    # 判断 category 的类别
    if feature_name.lower() in ["lon", "lat"]:
        category = "geo"
    elif feature_name.startswith('wc'):
        category = "clim"
    else:
        category = "soil"

    # 将每一行的字典添加到列表中
    data.append({
        "Feature": feature_name,
        "Importance": importance_value,
        "Category": category
    })

# 创建 DataFrame
importance_df = pd.DataFrame(data)

# 按 Importance 降序排列并保存为 CSV 文件
importance_df.sort_values(by='Importance', ascending=False).to_csv('data/model/feature_importances.csv', index=False)

# 13. 保存预测结果
predictions_df = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred
})
predictions_df.to_csv('data/model/predictions.csv', index=False)
