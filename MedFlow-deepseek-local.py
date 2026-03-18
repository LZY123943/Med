# coding=utf-8
import os
import requests
import re  # 新增导入re模块


def extract_privacy_from_txt(txt_dir="wenben/PICL4", output_dir="dk7privacy_results/PICL4"):
    """
    从TXT文件中提取文本并识别隐私信息
    """
    os.makedirs(output_dir, exist_ok=True)

    # Ollama配置
    OLLAMA_API_URL = ""
    MODEL_NAME = "deepseek-r1:7b"

    for filename in os.listdir(txt_dir):
        if not filename.endswith('.txt'):
            continue

        input_path = os.path.join(txt_dir, filename)
        output_path = os.path.join(output_dir, f"privacy_{filename}")

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text_content = f.read()

            # 保持原有prompt不变
            prompt = (f"请从以下医疗文本中提取隐私信息，直接返回结果文本：\n"
                      f"{text_content}\n"
                      f"要求：\n"
                      f"1. 隐私信息包括：患者姓名、姓名、性别、年龄、身份证号、手机号、住址、病历号、检查日期、医生姓名、检查医生、电话、职称、科室、医生签名、病人编号、检查编号、"
                      f"检查日期、门诊号、报告医生、报告日期、审核医生、出生日期、病历号、婚姻状况、职业、床号、民族、入院日期、出院日期、主治医生、护理人员\n"
                      f"2. 每行一个隐私信息项\n"
                      f"3. 示例格式(输出只要：后面的内容)：\n"
                      f"张三\n"
                      f"男\n"
                      f"35岁\n"
                      f"4. 只返回检测到的隐私信息，不要解释或其他内容，禁止输出未找到的字段，禁止使用无或任何占位符，病人的症状以及检测项目不属于隐私信息")

            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_ctx": 2048,
                        "repeat_penalty": 1.1
                    }
                },
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"API请求失败: {response.status_code} - {response.text}")

            # 提取原始输出
            raw_output = response.json().get("response", "").strip()

            # 新增：使用正则表达式移除<think>标签及其内容
            clean_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()

            # 保持原有的后处理逻辑，并加入去重
            seen = set()  # 用于记录已经出现过的行
            final_lines = []
            for line in clean_output.split('\n'):
                line = line.strip()
                if (
                        line  # 非空行
                        and not any(word in line for word in ["思考", "分析", "首先", "然后", "最后", "步骤"])  # 过滤思考过程
                        and line not in seen  # 去重
                ):
                    seen.add(line)  # 记录已出现的内容
                    final_lines.append(line)

            # 保存结果
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(final_lines))

            print(f"处理完成: {filename}")

        except Exception as e:
            print(f"处理文件{filename}时出错: {str(e)}")


if __name__ == '__main__':
    extract_privacy_from_txt()