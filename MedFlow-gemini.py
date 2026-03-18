# coding=utf-8
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def extract_privacy_text(text_content, log_file_path=None):
    """
    使用Gemini从文本内容中提取隐私信息
    :param text_content: 输入的文本内容
    :param log_file_path: 日志文件路径（可选）
    :return: 提取到的隐私信息文本
    """
    # 配置Gemini API
    genai.configure(
        api_key='',
        transport="rest",
        client_options={"api_endpoint": ""},
    )

    # 初始化模型
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 构建prompt
    prompt = f"""请从以下医疗文本中严格提取隐私信息，只需返回结果：

{text_content}

要求：
1. 只提取以下信息：患者姓名、姓名、性别、年龄、身份证号、手机号、住址、病历号、检查日期、医生姓名、检查医生、电话、职称、科室、医生签名、病人编号、检查编号、
              检查日期、门诊号、报告医生、报告日期、审核医生、出生日期、病历号、婚姻状况、职业、床号、民族、入院日期、出院日期、主治医生、护理人员
2. 每行一个隐私项，格式示例：
张三
男
35岁
110101199001011234
13800138000
3. 不要任何解释或额外文本"""

    try:
        # 调用Gemini API
        response = model.generate_content(prompt)

        # 获取响应文本
        privacy_text = response.text.strip()

        # 日志记录
        if log_file_path:
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"\n====== 隐私提取结果 ======\n")
                log_file.write(f"输入文本:\n{text_content}\n")
                log_file.write(f"输出隐私信息:\n{privacy_text}\n")

        return privacy_text

    except Exception as e:
        print(f"调用Gemini API时出错: {str(e)}")
        return ""


# process_txt_files函数保持不变...
def process_txt_files(input_dir="wenben/PICL1", output_dir="geiminiprivacy/PICL1"):
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