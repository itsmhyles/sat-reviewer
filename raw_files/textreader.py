import re
import json

def parse_questions(text):
    # Split text into individual questions using numbered pattern
    questions = re.split(r'\n(?=\d+\.)', text.strip())
    questions_data = []
    
    for i, q_text in enumerate(questions, 1):
        if not q_text.strip():
            continue
            
        # Extract question text
        question_pattern = r'.*?(?=(?:[A-D]\))|$)'
        question_match = re.search(question_pattern, q_text, re.DOTALL)
        question_text = question_match.group().strip() if question_match else ""
        
        # Extract choices
        choices = {}
        choices_pattern = r'([A-D]\))\s*(.*?)(?=[A-D]\)|QUESTION|$)'
        for match in re.finditer(choices_pattern, q_text, re.DOTALL):
            letter = match.group(1).strip(')')
            choice_text = match.group(2).strip()
            choices[letter] = choice_text
        
        # Extract explanation
        explanation_pattern = r'QUESTION.*?Choice ([A-D]) is the best answer because(.*?)(?=Choice [A-D]|$)'
        explanation_match = re.search(explanation_pattern, q_text, re.DOTALL)
        
        if explanation_match:
            correct_answer = explanation_match.group(1)
            explanation = explanation_match.group(2).strip()
            
            # Get incorrect explanations
            incorrect_pattern = r'Choice ([A-D]) is incorrect because(.*?)(?=Choice|$)'
            incorrect_explanations = {}
            
            for match in re.finditer(incorrect_pattern, q_text, re.DOTALL):
                letter = match.group(1)
                exp = match.group(2).strip()
                incorrect_explanations[letter] = exp
            
            question_obj = {
                "id": i,
                "question_text": ' '.join(question_text.split()),  # Combine multiple lines
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": {
                    "correct": ' '.join(explanation.split()),  # Combine multiple lines
                    "incorrect": {k: ' '.join(v.split()) for k, v in incorrect_explanations.items()}
                },
                "category": "Reading Comprehension",
                "difficulty": "medium"
            }
            questions_data.append(question_obj)
    
    return {"questions": questions_data}

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    json_structure = parse_questions(text)
    
    # Save to JSON file
    with open('question_bank.json', 'w', encoding='utf-8') as f:
        json.dump(json_structure, f, indent=4)
    
    return json_structure

#Usage
result = process_file('reading.txt')
print(json.dumps(result, indent=4))