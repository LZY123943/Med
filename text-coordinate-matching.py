# coding=utf-8
import os
import json


def parse_privacy_text(text_content):
    """
    解析纯文本隐私信息（每行一个值）
    输入示例：
    陈刚
    男
    李伟
    2025年2月21日
    """
    items = []
    for line in text_content.split('\n'):
        line = line.strip()
        if line:
            # 自动识别类型（简单实现，实际可增强）
            if '男' in line or '女' in line:
                items.append(('性别', line))
            elif '年' in line and '月' in line and '日' in line:
                items.append(('日期', line))
            else:
                items.append(('姓名', line))
    return items


def match_with_rag(privacy_items, rag_data):
    """
    将隐私项与RAG数据匹配
    """
    matched = []
    char_details = rag_data.get('character_details', [])
    text_blocks = rag_data.get('text_blocks', [])

    for item_type, item_value in privacy_items:
        for block in text_blocks:
            if item_value in block['text']:
                # 获取匹配字符的坐标
                matched_chars = [
                    {'char': c['char'], 'position': c['position']}
                    for c in char_details
                    if c['text_block'] == block['text'] and c['char'] in item_value
                ]

                if matched_chars:
                    matched.append({
                        'type': item_type,
                        'value': item_value,
                        'positions': [c['position'] for c in matched_chars],
                        'source_text': block['text']
                    })
                    break
    return matched


def process_files(privacy_dir="dk7privacy_results/PICL1", rag_dir="rag/PICL1", output_dir="deepseekresults/PICL1"):
    os.makedirs(output_dir, exist_ok=True)

    for privacy_file in os.listdir(privacy_dir):
        if not privacy_file.startswith('privacy_') or not privacy_file.endswith('.txt'):
            continue

        # 获取对应的RAG文件（新逻辑）
        base_name = privacy_file[8:]  # 移除'privacy_'前缀
        rag_file = f"{os.path.splitext(base_name)[0]}_rag.json"  # 替换为_rag.json
        rag_path = os.path.join(rag_dir, rag_file)

        if not os.path.exists(rag_path):
            print(f"缺少RAG文件: {rag_file} (查找路径: {rag_path})")
            continue

        # 读取隐私文本
        with open(os.path.join(privacy_dir, privacy_file), 'r', encoding='utf-8') as f:
            privacy_text = f.read()

        # 解析隐私文本
        privacy_items = parse_privacy_text(privacy_text)

        # 读取RAG数据
        with open(rag_path, 'r', encoding='utf-8') as f:
            rag_data = json.load(f)

        # 匹配坐标
        matched_data = match_with_rag(privacy_items, rag_data)

        # 保存结果
        output_name = f"{os.path.splitext(base_name)[0]}_matched.json"
        output_path = os.path.join(output_dir, output_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(matched_data, f, ensure_ascii=False, indent=2)

        print(f"生成: {output_path}")


if __name__ == '__main__':
    process_files()