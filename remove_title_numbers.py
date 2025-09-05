import os
import re

# 定义要处理的目录
base_dir = r"d:\Git\docs\docs\manual\admin"

# 匹配标题序号的正则表达式
# 匹配 ## 数字. 标题 或 ### 数字.数字 标题 等模式
pattern = re.compile(r'^(#+)\s+(\d+(?:\.\d+)*\.?)\s+(.+)$', re.MULTILINE)

def remove_title_numbers(content):
    """移除标题中的序号"""
    def replace_func(match):
        hash_marks = match.group(1)  # ## 或 ###
        title_text = match.group(3)  # 标题文本
        return f"{hash_marks} {title_text}"
    
    return pattern.sub(replace_func, content)

def process_md_files(directory):
    """处理目录下的所有markdown文件"""
    processed_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 移除标题序号
                    new_content = remove_title_numbers(content)
                    
                    # 如果内容有变化，写回文件
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        processed_files.append(file_path)
                        print(f"已处理: {file_path}")
                
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")
    
    return processed_files

if __name__ == "__main__":
    print(f"开始处理目录: {base_dir}")
    processed = process_md_files(base_dir)
    print(f"\n共处理了 {len(processed)} 个文件")
    for file in processed:
        print(f"- {file}")
