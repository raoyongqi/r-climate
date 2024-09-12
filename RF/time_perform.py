import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')  # 使用 TkAgg 作为交互式后端
# 模型数据
models = ['Model 1', 'Model 2', 'Model 3']
accuracy = [0.85, 0.82, 0.88]
time = [120, 100, 150]

# 绘制散点图
plt.figure(figsize=(8, 6))
plt.scatter(time, accuracy, color='blue')

# 为每个点添加标签
for i, model in enumerate(models):
    plt.text(time[i], accuracy[i], model)

# 添加标题和标签
plt.title('Performance vs Time')
plt.xlabel('Training Time (seconds)')
plt.ylabel('Accuracy')

plt.show()
