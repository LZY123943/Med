# coding=utf-8
import os
from openai import OpenAI
from dotenv import load_dotenv  # 用于管理API密钥

# 加载环境变量（从.env文件读取API密钥）
load_dotenv()

def extract_privacy_text(text_content, log_file_path=None):
    """
    从文本内容中提取隐私信息
    :param text_content: 输入的文本内容
    :param log_file_path: 日志文件路径（可选）
    :return: 提取到的隐私信息文本
    """
    client = OpenAI(api_key=''
                    ,base_url = '',
                    timeout=60.0)  # 替换为实际API密钥

    # 构建简洁的prompt
    prompt = (f"请从以下医疗文本中提取隐私信息，直接返回结果文本：\n"
              f"{text_content}\n"
              f"要求：\n"
              f"1. 隐私信息包括：患者姓名、姓名、性别、年龄、身份证号、手机号、住址、病历号、检查日期、医生姓名、检查医生、电话、职称、科室、医生签名、病人编号、检查编号、"
              f"检查日期、门诊号、报告医生、报告日期、审核医生、出生日期、病历号、婚姻状况、职业、床号、民族、入院日期、出院日期、主治医生、护理人员\n"
              f"2. 每行一个隐私信息项\n"
              f"3. 示例格式：\n"
              f"张三\n"
              f"男\n"
              f"35岁\n"
              f"110101199001011234\n"
              f"4. 只返回检测到的隐私信息，不要解释或其他内容")

    try:
        # 调用大模型
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个专业的医疗隐私信息提取助手，直接返回最简洁的结果"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1  # 降低随机性
        )

        # 获取输出结果
        privacy_text = completion.choices[0].message.content.strip()

        # 日志记录（可选）
        if log_file_path:
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"\n====== 隐私提取结果 ======\n")
                log_file.write(f"输入文本:\n{text_content}\n")
                log_file.write(f"输出隐私信息:\n{privacy_text}\n")

        return privacy_text

    except Exception as e:
        print(f"调用OpenAI API时出错: {str(e)}")
        return ""

def process_txt_files(input_dir="wenben/PICL1", output_dir="privacy/PICL1"):
    """
    处理目录下的所有TXT文件
    :param input_dir: 输入目录（存放TXT文件）
    :param output_dir: 输出目录（存放隐私提取结果）
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 处理所有TXT文件
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue

        input_path = os.path.join(input_dir, filename)
        output_filename = f"{os.path.splitext(filename)[0]}_privacy.txt"
        output_path = os.path.join(output_dir, output_filename)

        try:
            # 读取TXT文件内容
            with open(input_path, 'r', encoding='utf-8') as f:
                text_content = f.read()

            # 调用隐私提取函数
            privacy_text = extract_privacy_text(text_content)

            # 保存提取结果
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(privacy_text)

            print(f"处理完成: {filename} -> {output_filename}")

        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")

if __name__ == '__main__':
    process_txt_files()  # 执行主函数