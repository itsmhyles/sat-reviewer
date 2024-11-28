# menu_handler.py
from session_manager import SessionFactory, run_simulation_session


class DisplayFormatter:
    @staticmethod
    def format_header(text):
        return f"\n{'='*50}\n{text.center(50)}\n{'='*50}"
    
    @staticmethod
    def format_question(number, total, question_text):
        return f"\nQuestion {number} of {total}\n\n{question_text}"
    
    @staticmethod
    def format_explanation(explanation_dict):
        formatted = "\nExplanation:"
        formatted += f"\n{'-'*50}\n"
        formatted += f"Correct Answer Explanation:\n{explanation_dict['correct']}\n"
        
        if 'incorrect' in explanation_dict:
            formatted += f"\nWhy other choices are incorrect:\n{'-'*30}\n"
            for choice, reason in explanation_dict['incorrect'].items():
                formatted += f"\nChoice {choice}:\n{reason}\n"
        return formatted
    
    @staticmethod
    def format_result(is_correct):
        return "\n✓ CORRECT!" if is_correct else "\n✗ INCORRECT!"
    
    @staticmethod
    def format_session_end(score, total):
        return f"\n{'='*50}\nSession completed!\nFinal Score: {score}/{total}\n{'='*50}"


class MenuHandler:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.formatter = DisplayFormatter()  
        
    def display_main_menu(self):
        while True:
            print("\n=== SAT Review System ===")
            print("1. Math")
            print("2. Reading and Writing")
            print("3. Combined")
            print("4. Exit")
            
            choice = input("\nSelect a section (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                if choice == '4':
                    return None
                return self._get_section_type(choice)
            print("Invalid choice. Please select 1-4.")
    
    def display_mode_menu(self):
        while True:
            print("\n=== Review Mode ===")
            print("1. Simulation Mode (Timed)")
            print("2. Chill Review Mode")
            print("3. Back to Main Menu")
            
            choice = input("\nSelect mode (1-3): ").strip()
            if choice in ['1', '2', '3']:
                if choice == '3':
                    return None
                return 'simulation' if choice == '1' else 'chill'
            print("Invalid choice. Please select 1-3.")

    def display_order_menu(self):
        while True:
            print("\n=== Question Order ===")
            print("1. Math First")
            print("2. Reading First")
            print("3. Back to Main Menu")
            
            choice = input("\nSelect order (1-3): ").strip()
            if choice in ['1', '2', '3']:
                if choice == '3':
                    return None
                return 'math_first' if choice == '1' else 'reading_first'
            print("Invalid choice. Please select 1-3.")
    
    def _get_section_type(self, choice):
        return {
            '1': 'math',
            '2': 'reading',
            '3': 'combined'
        }[choice]
    
    def run(self):
        while True:
            section_type = self.display_main_menu()
            if not section_type:
                print("\nThank you for using SAT Review System!")
                break
                
            mode = self.display_mode_menu()
            if not mode:
                continue
            
            # Get question order for combined sections
            order_preference = None
            if section_type == 'combined':
                order_preference = self.display_order_menu()
                if not order_preference:
                    continue
            
            session = self.session_factory.create_session(
                section_type=section_type,
                mode=mode,
                order_preference=order_preference
            )
            
            if mode == 'simulation':
                run_simulation_session(session.questions, session.session_type)
            else:
                self._run_chill_session(session)
        
    def _run_chill_session(self, session):
        print(self.formatter.format_header(f"Starting {session.session_type} chill review"))
        print(f"Total questions: {session.total_questions}")
        
        while True:
            question = session.get_current_question()
            if not question:
                break
            
            # Only use the formatter to display the question and choices
            print(self.formatter.format_question(
                session.current_question_index + 1,
                session.total_questions,
                question.question_text
            ))
            
            # Display only the choices, not the question again
            for letter, choice in question.choices.items():
                print(f"{letter}) {choice}")
            
            answer = input("\nYour answer (A/B/C/D): ").upper()
            while answer not in ['A', 'B', 'C', 'D']:
                print("Invalid input. Please enter A, B, C, or D.")
                answer = input("Your answer (A/B/C/D): ").upper()
            
            is_correct = session.submit_answer(answer)
            print(self.formatter.format_result(is_correct))
            print(self.formatter.format_explanation(session.show_explanation()))
            
            input("\nPress Enter to continue...")
        
        print(self.formatter.format_session_end(session.score, session.total_questions))