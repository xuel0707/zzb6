if True:
    import pdfplumber
    import json
    import os
    import argparse

    def extract_text_from_pdf(pdf_path):
        all_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text()
                        if text:  # 如果有提取到的文本
                            all_text += text.strip() + "\n"  # 合并文本，并在每个页面后添加换行符分隔
                    except Exception as e:
                        print(f"Error extracting page {page_num} from {pdf_path}: {e}")
        except Exception as e:
            print(f"Error opening PDF file {pdf_path}: {e}")
        
        return {
            "text": all_text.strip()  # 去除最后可能多余的换行符
        }

    def save_to_json(data, json_path):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def process_pdfs_in_directory(directory_path, output_json_path):
        all_data = []
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                print(f"Processing {pdf_path}")
                extracted_data = extract_text_from_pdf(pdf_path)
                all_data.append(extracted_data)
        
        save_to_json(all_data, output_json_path)

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Process PDFs in a directory and convert them to JSON format.")
        parser.add_argument('directory_path', type=str, help='The directory containing the PDF files.')
        parser.add_argument('output_json_path', type=str, help='The path to the output JSON file.')

        args = parser.parse_args()

        if not os.path.isdir(args.directory_path):
            print(f"The provided directory path '{args.directory_path}' does not exist or is not a directory.")
        else:
            process_pdfs_in_directory(args.directory_path, args.output_json_path)    
else:
    import pdfplumber
    import json
    import os
    import argparse

    def extract_text_from_pdf(pdf_path):
        pages_text = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text()
                        if text and text.strip():  # 如果页面有非空白文本
                            pages_text.append({
                                "text": text.strip()
                            })
                        else:
                            print(f"Skipped empty page {page_num} from {pdf_path}")
                    except Exception as e:
                        print(f"Error extracting page {page_num} from {pdf_path}: {e}")
        except Exception as e:
            print(f"Error opening PDF file {pdf_path}: {e}")
        
        return pages_text

    def save_to_json(data, json_path):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def process_pdfs_in_directory(directory_path, output_json_path):
        all_data = []
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                print(f"Processing {pdf_path}")
                pages = extract_text_from_pdf(pdf_path)
                all_data.extend(pages)  # 只添加非空页
        
        save_to_json(all_data, output_json_path)

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Process PDFs in a directory and convert them to JSON format, one non-empty page per entry.")
        parser.add_argument('directory_path', type=str, help='The directory containing the PDF files.')
        parser.add_argument('output_json_path', type=str, help='The path to the output JSON file.')

        args = parser.parse_args()

        if not os.path.isdir(args.directory_path):
            print(f"The provided directory path '{args.directory_path}' does not exist or is not a directory.")
        else:
            process_pdfs_in_directory(args.directory_path, args.output_json_path)
        
    