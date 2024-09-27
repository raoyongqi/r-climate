import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib
import os
import shap
import matplotlib.pyplot as plt

# 1. 读取Excel文件
file_path = 'data/output_data.xlsx'
data = pd.read_excel(file_path)

# 2. 筛选特征列
feature_columns = [col for col in data.columns if col.endswith('_resampled') or col.lower().startswith('wc') or col in ['LON', 'LAT']]
print(feature_columns)

# 3. 分离特征变量和目标变量
X = data[feature_columns]
y = data['PL']  # 目标变量

# 4. 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 初始化并训练XGBoost回归模型
xgb_model = XGBRegressor(n_estimators=100, random_state=42, learning_rate=0.1, max_depth=6)
xgb_model.fit(X_train, y_train)

# 6. 预测并评估模型
y_pred = xgb_model.predict(X_test)

# 7. 评估模型性能
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 输出结果
print(f"均方误差 (MSE): {mse:.4f}")
print(f"R² 得分: {r2:.4f}")

# 8. 确保保存路径存在
os.makedirs('data/model', exist_ok=True)

# 9. 保存模型
joblib.dump(xgb_model, 'data/model/xgboost_model.pkl')

# 12. 计算 SHAP 值并绘制 SHAP 图
explainer = shap.Explainer(xgb_model, X_train)
shap_values = explainer(X_test)

shap.summary_plot(shap_values, X_test, max_display=10, show=False, cmap='PiYG')

# 保存 SHAP 图
plt.savefig('data/model/shap_summary_plot.png', bbox_inches='tight')  # 使用 bbox_inches='tight' 确保内容完整

# 关闭图形
plt.close()
