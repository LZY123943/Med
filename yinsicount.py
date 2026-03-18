import os


def count_lines_in_file(file_path):
    """计算单个文件的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"处理文件 {file_path} 出错: {str(e)}")
        return 0


def count_lines_in_directory(directory):
    """计算目录下所有TXT文件的行数"""
    total_lines = 0
    print(f"\n检查目录: {directory}")
    print("-" * 40)

    for filename in os.listdir(directory):
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(directory, filename)
        line_count = count_lines_in_file(file_path)
        total_lines += line_count

        print(f"{filename:<30} : {line_count} 行")

    print("-" * 40)
    print(f"目录 {os.path.basename(directory)} 总行数: {total_lines}")
    return total_lines


def count_all_txt_lines(main_directory="dk7privacy_results"):
    """统计主目录下所有子目录的TXT文件行数"""
    if not os.path.exists(main_directory):
        print(f"主目录不存在: {main_directory}")
        return

    print(f"\n开始检查主目录: {main_directory}")
    print("=" * 40)

    total_all_lines = 0
    subdirs = [d for d in os.listdir(main_directory)
               if os.path.isdir(os.path.join(main_directory, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(main_directory, subdir)
        subdir_lines = count_lines_in_directory(subdir_path)
        total_all_lines += subdir_lines

    print("\n" + "=" * 40)
    print(f"所有子目录TXT文件总行数: {total_all_lines}")
    print("=" * 40)


if __name__ == '__main__':
    count_all_txt_lines()