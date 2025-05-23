import json
import argparse

def summarize_support_content(text):
    """
    根据文本内容提取“申请内容”或“支持内容”部分。
    这里只是一个简单的字符串匹配示例，实际可使用NLP或正则进一步优化。
    """
    start_keywords = ["申请内容", "支持内容", "一、申请内容", "一、支持内容"]
    end_keywords = ["设定依据", "二、设定依据", "二、支持强度与方式"]

    start_idx = -1
    end_idx = -1

    # 找到起始位置
    for keyword in start_keywords:
        idx = text.find(keyword)
        if idx != -1:
            start_idx = idx
            break

    # 找到结束位置
    for keyword in end_keywords:
        idx = text.find(keyword, start_idx + 100)  # 向后搜索避免重叠
        if idx != -1:
            end_idx = idx
            break

    if start_idx != -1:
        summary_text = text[start_idx:start_idx + (end_idx - start_idx if end_idx != -1 else 500)]
        lines = summary_text.split("。")
        bullet_points = "\n".join([f"{i + 1}. {line.strip()}" for i, line in enumerate(lines) if line.strip()])
        return bullet_points
    else:
        return "无法提取支持内容摘要。"

def convert_json_format(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_path, 'w', encoding='utf-8') as out_f:
        for item in data:
            raw_text = item.get('text', '').strip()
            if not raw_text:
                continue

            instruction = "请阅读以下政策文本，总结出该项目的支持内容。"
            input_text = raw_text[:4096]  # 防止过长，限制输入长度
            output_summary = summarize_support_content(raw_text)

            sample = {
                "instruction": instruction,
                "input": input_text,
                "output": output_summary
            }

            out_f.write(json.dumps(sample, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert policy JSON to fine-tuning format.")
    parser.add_argument('--input_json', type=str, required=True, help='Path to the input JSON file.')
    parser.add_argument('--output_json', type=str, required=True, help='Path to the output JSON file.')

    args = parser.parse_args()

    convert_json_format(args.input_json, args.output_json)