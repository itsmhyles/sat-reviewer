import json

# questions/question_handler.py

class Question:
    """
    Represents a single question in the question bank.

    Attributes:
        id (str): Unique identifier for the question.
        question_text (str): The text of the question.
        choices (dict): A dictionary of answer choices.
        correct_answer (str): The correct answer to the question.
        explanation (str): Explanation for the correct answer.
        category (str): The category of the question.
        difficulty (str): The difficulty level of the question.
    """

    def __init__(self, id, question_text, choices, correct_answer, explanation, category, difficulty):
        self.id = id
        self.question_text = question_text
        self.choices = choices
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.category = category
        self.difficulty = difficulty
    
    def display(self):
        """
        Displays the question text and answer choices.
        """
        print("\nQuestion:", self.question_text)
        for letter, choice in self.choices.items():
            print(f"{letter}) {choice}")


class QuestionBank:
    """
    Manages a collection of questions for different sections.

    Attributes:
        math_questions (list): List of math questions.
        reading_questions (list): List of reading questions.
        categories (set): Set of unique categories across all questions.
        difficulties (set): Set of unique difficulty levels across all questions.
    """

    def __init__(self):
        self.math_questions = []
        self.reading_questions = []
        self.categories = set()
        self.difficulties = set()
    
    def load_questions(self, json_file, section_type):
        """
        Loads questions from a JSON file into the question bank.

        Args:
            json_file (str): Path to the JSON file containing questions.
            section_type (str): Type of questions ('math' or 'reading').

        Returns:
            bool: True if questions were loaded successfully, False otherwise.
        """
        try:
            with open(json_file, 'r', encoding='utf-8-sig') as file:
                data = json.load(file)
                questions = []
                for item in data['questions']:
                    question = Question(
                        id=item['id'],
                        question_text=item['question_text'],
                        choices=item['choices'],
                        correct_answer=item['correct_answer'],
                        explanation=item['explanation'],
                        category=item.get('category', 'Unknown'),
                        difficulty=item.get('difficulty', 'medium')
                    )
                    questions.append(question)
                    self.categories.add(question.category)
                    self.difficulties.add(question.difficulty)
                
                # Add questions to the appropriate section
                if section_type == 'math':
                    self.math_questions.extend(questions)
                else:
                    self.reading_questions.extend(questions)
                
                return True
        except FileNotFoundError:
            print(f"Error: Could not find {json_file}")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {json_file}")
            return False


class QuestionManager:
    """
    Manages question selection and session handling.

    Attributes:
        question_bank (QuestionBank): The question bank to manage.
        current_session (Any): Placeholder for current session data (not implemented in this code).
    """

    def __init__(self, question_bank):
        self.question_bank = question_bank
        self.current_session = None
    
    def get_questions_by_section(self, section_type, difficulty=None):
        """
        Retrieves questions from a specific section and optionally filters by difficulty.

        Args:
            section_type (str): The type of questions to retrieve ('math' or 'reading').
            difficulty (str, optional): The difficulty level to filter by.

        Returns:
            list: A list of Question objects matching the criteria.
        """
        questions = (self.question_bank.math_questions if section_type == 'math' 
                    else self.question_bank.reading_questions)
        
        if difficulty:
            questions = [q for q in questions if q.difficulty == difficulty]
        
        return questions
    
    def shuffle_questions(self, questions, count=None):
        """
        Shuffles a list of questions and optionally limits the number of questions returned.

        Args:
            questions (list): The list of questions to shuffle.
            count (int, optional): The number of questions to return after shuffling.

        Returns:
            list: A shuffled list of questions, optionally limited to 'count' items.
        """
        import random
        shuffled = questions.copy()
        random.shuffle(shuffled)
        return shuffled[:count] if count else shuffled


# Initialize the system
question_bank = QuestionBank()
question_bank.load_questions('math_1.json', 'math')
question_bank.load_questions('reading_1.json', 'reading')

# Create question manager
manager = QuestionManager(question_bank)
