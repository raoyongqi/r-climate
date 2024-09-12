import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler

# 1. 读取Excel文件
file_path = 'data/output_data.xlsx'
data = pd.read_excel(file_path)

# 2. 筛选特征列：以 '_resampled' 结尾，'wc' 开头（不区分大小写），以及 'LON' 和 'LAT' 列
feature_columns = [col for col in data.columns if col.endswith('_resampled') or col.lower().startswith('wc') or col in ['LON', 'LAT']]

# 3. 分离特征变量和目标变量
X = data[feature_columns]
y = data['PL']  # 目标变量

# 4. 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. 构建神经网络模型
model = Sequential()
model.add(Dense(64, input_dim=X_train_scaled.shape[1], activation='relu'))  # 输入层和隐藏层
model.add(Dense(32, activation='relu'))  # 第二隐藏层
model.add(Dense(1))  # 输出层

# 7. 编译模型
model.compile(loss='mean_squared_error', optimizer='adam')

# 8. 训练模型
model.fit(X_train_scaled, y_train, epochs=50, batch_size=10, verbose=1)

# 9. 预测并评估模型
y_pred_nn = model.predict(X_test_scaled)

# 10. 评估神经网络模型性能
mse_nn = mean_squared_error(y_test, y_pred_nn)
r2_nn = r2_score(y_test, y_pred_nn)

# 输出结果
print(f"神经网络的均方误差 (MSE): {mse_nn:.4f}")
print(f"神经网络的R² 得分: {r2_nn:.4f}")

# 11. 保存预测结果
predictions_nn_df = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred_nn.flatten()
})
predictions_nn_df.to_csv('data/model/predictions_nn.csv', index=False)
