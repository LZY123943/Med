import json
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from pathlib import Path

def get_character_positions(text_data):
    """
    分析文本中每个字符的位置
    返回格式: [{"char": 字符, "position": [x1,y1,x2,y2]}, ...]
    """
    character_data = []
    for item in text_data:
        text = item["text"]
        x1, y1 = item["top_left"]
        x2, y2 = item["bottom_right"]

        # 计算每个字符的宽度
        char_width = (x2 - x1) / len(text)

        # 为每个字符计算位置
        for i, char in enumerate(text):
            char_x1 = x1 + i * char_width
            char_x2 = x1 + (i + 1) * char_width
            character_data.append({
                "char": char,
                "position": [round(char_x1, 1), round(y1, 1), round(char_x2, 1), round(y2, 1)]
            })

    return character_data

# 注释掉可视化函数
# def visualize_on_image(image_path, character_data, output_path):
#     """
#     在图片上可视化字符位置
#     """
#     # 打开原始图片
#     img = Image.open(image_path)
#     draw = ImageDraw.Draw(img)
#
#     # 设置字体（需要根据系统调整）
#     try:
#         font = ImageFont.truetype("simsun.ttc", 20)
#     except:
#         font = ImageFont.load_default()
#
#     # 绘制每个字符的边界框
#     for char_info in character_data:
#         char = char_info["char"]
#         x1, y1, x2, y2 = char_info["position"]
#
#         # 绘制矩形框
#         draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
#
#         # 在框上方显示字符
#         draw.text((x1, y1 - 25), char, fill="blue", font=font)
#
#     # 保存结果图片
#     img.save(output_path)
#     print(f"可视化结果已保存到: {output_path}")

def process_json_file(json_path, image_dir, output_dir, visual_dir):
    """
    处理单个JSON文件
    """
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        text_data = json.load(f)

    # 获取字符级位置信息
    character_data = get_character_positions(text_data)

    # 保存字符级位置信息
    char_json_path = os.path.join(output_dir, f"char_{os.path.basename(json_path)}")
    with open(char_json_path, 'w', encoding='utf-8') as f:
        json.dump(character_data, f, ensure_ascii=False, indent=4)
    print(f"字符级位置信息已保存到: {char_json_path}")

    # 注释掉可视化步骤
    # # 可视化结果（需要原始图片）
    # image_filename = os.path.splitext(os.path.basename(json_path))[0] + ".jpg"
    # image_path = os.path.join(image_dir, image_filename)
    # if os.path.exists(image_path):
    #     output_image_path = os.path.join(visual_dir, f"vis_{image_filename}")
    #     visualize_on_image(image_path, character_data, output_image_path)

def main():
    # 设置路径
    json_dir = "ocr/PICL4"          # 存放OCR结果的JSON文件目录
    image_dir = "data/PICL4"     # 原始图片目录
    output_dir = "char_positions/PICL4"  # 字符坐标输出目录
    visual_dir = "chartu/PICL2"     # 可视化图片输出目录（虽然不使用但仍保留参数）

    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Path(visual_dir).mkdir(parents=True, exist_ok=True)  # 不再需要创建可视化目录

    # 处理所有JSON文件
    for json_file in os.listdir(json_dir):
        if json_file.endswith(".json"):
            json_path = os.path.join(json_dir, json_file)
            print(f"\n正在处理文件: {json_file}")
            process_json_file(json_path, image_dir, output_dir, visual_dir)

    print("\n所有文件处理完成！")

if __name__ == "__main__":
    main()