# menu_handler.py
from session_manager import SessionFactory, run_simulation_session

class MenuHandler:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        
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
                
            session = self.session_factory.create_session(
                section_type=section_type,
                mode=mode,
                question_count=10
            )
            
            if mode == 'simulation':
                run_simulation_session(session.questions, session.session_type)
            else:
                self._run_chill_session(session)
    
    def _run_chill_session(self, session):
        print(f"\nStarting {session.session_type} chill review")
        print(f"Total questions: {session.total_questions}")
        
        while True:
            question = session.get_current_question()
            if not question:
                break
                
            print(f"\nQuestion {session.current_question_index + 1} of {session.total_questions}")
            question.display()
            
            answer = input("\nYour answer (A/B/C/D): ").upper()
            while answer not in ['A', 'B', 'C', 'D']:
                print("Invalid input. Please enter A, B, C, or D.")
                answer = input("Your answer (A/B/C/D): ").upper()
            
            is_correct = session.submit_answer(answer)
            print("\n✓ Correct!" if is_correct else "\n✗ Incorrect!")
            print("Explanation:", session.show_explanation())
            
            input("\nPress Enter to continue...")
        
        print(f"\nSession completed! Score: {session.score}/{session.total_questions}")