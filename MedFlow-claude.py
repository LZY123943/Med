# coding=utf-8
import os
from openai import OpenAI
from dotenv import load_dotenv  # 用于管理API密钥
from anthropic import Anthropic
# 加载环境变量（从.env文件读取API密钥）
load_dotenv()


def extract_privacy_text(text_content, log_file_path=None):
    """
    使用Claude 3从文本内容中提取隐私信息
    :param text_content: 输入的文本内容
    :param log_file_path: 日志文件路径（可选）
    :return: 提取到的隐私信息文本
    """
    # 初始化Claude客户端
    client = Anthropic(
        api_key=''
        # 如果使用代理，确保代理端点支持Claude API
    , base_url = '',
    )

    # 构建prompt（Claude推荐使用XML标签格式）
    prompt = f"""<task>
请从以下医疗文本中提取隐私信息：

<text>
{text_content}
</text>

<requirements>
1. 提取以下隐私信息：隐私信息包括：患者姓名、姓名、性别、年龄、身份证号、手机号、住址、病历号、检查日期、医生姓名、检查医生、电话、职称、科室、医生签名、病人编号、检查编号、
              检查日期、门诊号、报告医生、报告日期、审核医生、出生日期、病历号、婚姻状况、职业、床号、民族、入院日期、出院日期、主治医生、护理人员
2. 每行一个隐私项，格式示例：
张三
男
35岁
110101199001011234
13800138000
3. 只返回检测到的信息，不要解释
</requirements>
</task>"""

    try:
        # 调用Claude 3 API（注意正确的参数格式）
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system="你是一个专业的医疗隐私信息提取助手，请严格按要求格式返回结果",  # system提示作为独立参数
            messages=[{"role": "user", "content": prompt}],  # 只需要user消息
            temperature=0.1
        )

        # 获取并清理响应
        privacy_text = response.content[0].text.strip()

        # 日志记录
        if log_file_path:
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"\n====== 隐私提取结果 ======\n")
                log_file.write(f"输入文本:\n{text_content}\n")
                log_file.write(f"输出隐私信息:\n{privacy_text}\n")

        return privacy_text

    except Exception as e:
        print(f"调用Claude API时出错: {str(e)}")  # 修正错误提示
        return ""
def process_txt_files(input_dir="wenben/PICL4", output_dir="claudeprivacy/PICL4"):
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