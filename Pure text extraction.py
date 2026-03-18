import os
import json

# 定义路径
input_dir = 'ocr/PICL4'  # 存放 JSON 文件的目录
output_dir = 'wenben/PICL4'  # 存放 TXT 文件的目录

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 遍历 PICL1 目录下的所有 JSON 文件
for json_file in os.listdir(input_dir):
    if json_file.endswith('.json'):
        json_path = os.path.join(input_dir, json_file)
        txt_filename = os.path.splitext(json_file)[0] + '.txt'  # 替换扩展名
        txt_path = os.path.join(output_dir, txt_filename)

        try:
            # 读取 JSON 文件
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 提取所有 "text" 字段并按顺序拼接
            text_content = "\n".join([item.get("text", "") for item in data if "text" in item])

            # 写入 TXT 文件
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text_content)

            print(f"成功提取 {json_file} 并保存为 {txt_filename}")

        except json.JSONDecodeError:
            print(f"错误：{json_file} 不是有效的 JSON 文件")
        except Exception as e:
            print(f"处理 {json_file} 时出错: {str(e)}")

print("所有 JSON 文件处理完成！")