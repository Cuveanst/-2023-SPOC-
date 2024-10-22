import json

with open('原始题库.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

questions = []
current_question = ""
in_question = False
options = {}  # 用于存储当前题目的选项，字典形式存储选项字母和对应的文本

# 遍历
for i, line in enumerate(lines):
    line = line.strip()

    if line == '':  # 跳过空行
        continue

    if (("单选题" in line) or ("多选题" in line)):
        current_question = lines[i + 1].strip()
        in_question = True
        options = {}  # 重置

    elif "教师评语：" in line:
        # 检查是否有足够的行数，避免索引超出范围
        if i + 4 < len(lines) and not any(prefix in lines[i + 4].strip() for prefix in ["单选题", "多选题", "判断题"]):
            if not lines[i + 4].strip()[0].isdigit():
                current_question = lines[i + 4].strip()
                in_question = True
                options = {}  # 重置

    elif in_question:
        if len(line) >= 2 and line[0] in ['A', 'B', 'C', 'D'] and line[1] == '.':
            option_letter = line[0]
            option_text = line[2:].strip()
            if not option_text:
                option_text = lines[i + 2].strip()
            #字典存储
            options[option_letter] = option_text


        elif "正确答案" in line:
            correct_letters = lines[i + 2].strip()
            correct_answer_text = []
            
            for letter in correct_letters.split():
                if letter in options:
                    correct_answer_text.append(options[letter])

            # 合并答案
            if correct_answer_text:
                correct_answer_text = "==".join(correct_answer_text)
            else:
                correct_answer_text = "未找到正确答案"

            print(f'Q:{current_question}, A:{correct_answer_text}')
            

            questions.append({
                "question": current_question,
                "correct_answer": correct_answer_text,
            })
            
            # reset status
            current_question = ""
            in_question = False


with open('exam_questions_and_answers.json', 'w', encoding='utf-8') as json_file:
    json.dump(questions, json_file, ensure_ascii=False, indent=4)

print("提取完成，文件已保存为 'exam_questions_and_answers.json'")
