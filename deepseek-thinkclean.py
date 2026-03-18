import os
import json


def clean_json_file(file_path):
    """清理JSON文件的第一行和最后一行"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 确保文件至少有3行（第一行、JSON内容和最后一行）
        if len(lines) < 3:
            raise ValueError("文件行数不足，无法清理")

        # 移除第一行和最后一行
        cleaned_lines = lines[1:-1]
        cleaned_content = ''.join(cleaned_lines)

        # 验证JSON格式是否正确
        json.loads(cleaned_content)

        # 重新写入清理后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        return True

    except json.JSONDecodeError as e:
        print(f"文件 {os.path.basename(file_path)} 清理后仍不是有效JSON: {str(e)}")
        return False
    except Exception as e:
        print(f"处理文件 {os.path.basename(file_path)} 出错: {str(e)}")
        return False


def process_directory(directory):
    """处理目录下的所有JSON文件"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"正在处理: {file_path}")
                if clean_json_file(file_path):
                    print(f"成功清理: {file}")
                else:
                    print(f"清理失败: {file}")


if __name__ == '__main__':
    # 指定要处理的目录
    target_directory = "geminiprivacyjiu"  # 修改为您的目录路径

    if os.path.exists(target_directory):
        print(f"开始处理目录: {target_directory}")
        process_directory(target_directory)
        print("处理完成！")
    else:
        print(f"目录不存在: {target_directory}")