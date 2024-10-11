import codecs

# 读取带 BOM 的文件并去除 BOM
with codecs.open('C:\Users\r\Desktop\word\pic\climate_data.csv', 'r', 'utf-8-sig') as file:
    content = file.read()

# 保存去掉 BOM 的文件
with open('C:\Users\r\Desktop\word\pic\climate_data_no_bom.csv', 'w', encoding='utf-8') as file:
    file.write(content)

print("BOM 已删除")
