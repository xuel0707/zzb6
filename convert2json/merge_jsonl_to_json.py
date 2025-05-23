import json
import glob
import os

def merge_jsonl_files(input_dir, output_file):
    """
    将指定目录下的所有 .jsonl 文件合并为一个 JSON 数组文件，采用流式处理以减少内存占用。
    
    :param input_dir: 包含 jsonl 文件的目录路径
    :param output_file: 合并后的输出文件路径
    """
    jsonl_files = sorted(glob.glob(os.path.join(input_dir, "*.jsonl")))
    if not jsonl_files:
        print("No .jsonl files found in the directory.")
        return
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 开始 JSON 数组
        outfile.write('[\n')
        
        first_file = True
        for jsonl_file in jsonl_files:
            print(f"Processing {jsonl_file} ...")
            first_line_in_file = True
            with open(jsonl_file, 'r', encoding='utf-8') as infile:
                for line in infile:
                    if line.strip():
                        if not first_file or not first_line_in_file:
                            outfile.write(',\n')
                        else:
                            if not first_line_in_file:
                                outfile.write(',\n')
                        outfile.write(line.rstrip())
                        first_line_in_file = False
            first_file = False
        
        # 结束 JSON 数组
        outfile.write('\n]')
        print(f"Merged JSON saved to {output_file}")

# 示例调用
if __name__ == "__main__":
    input_dir = "/mnt/outputs/sft/merge"  # 替换为你自己的 jsonl 文件夹路径
    output_file = "/mnt/qwen-datasets/qwen_sft.json"  # 输出文件路径
    merge_jsonl_files(input_dir, output_file)
