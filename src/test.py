import pickle
# --- 序列化 ---

dict = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}

f = open("pickle.txt", "wb+")

# 写入
pickle.dump(dict, f)  # 序列化到文件

# 关闭
f.close()

# --- 反序列化 ---
f = open("pickle.txt", "rb+")

# 读取
data = pickle.load(f)  # 从文件反序列化
print(data)
f.close()


data['Cecil'] = 8;
f = open("pickle.txt", "wb+")
# 写入
pickle.dump(data, f)  # 序列化到文件
# 关闭
f.close()



# --- 反序列化 ---
f = open("pickle.txt", "rb+")

# 读取
data = pickle.load(f)  # 从文件反序列化
print(data)
f.close()


