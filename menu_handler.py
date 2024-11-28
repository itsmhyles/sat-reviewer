# menu_handler.py
from session_manager import SessionFactory, run_simulation_session


class DisplayFormatter:
    """
    A utility class for formatting various display elements in the SAT Review System.
    """

    @staticmethod
    def format_header(text):
        """
        Formats a header with centered text surrounded by equal signs.

        Args:
            text (str): The text to be centered in the header.

        Returns:
            str: A formatted header string.
        """
        return f"\n{'='*50}\n{text.center(50)}\n{'='*50}"
    
    @staticmethod
    def format_question(number, total, question_text):
        """
        Formats a question display with question number and text.

        Args:
            number (int): The current question number.
            total (int): The total number of questions.
            question_text (str): The text of the question.

        Returns:
            str: A formatted question string.
        """
        return f"\nQuestion {number} of {total}\n\n{question_text}"
    
    @staticmethod
    def format_explanation(explanation_dict):
        """
        Formats the explanation for a question, including correct and incorrect answer explanations.

        Args:
            explanation_dict (dict): A dictionary containing explanations for correct and incorrect answers.

        Returns:
            str: A formatted explanation string.
        """
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
        """
        Formats the result of an answer submission.

        Args:
            is_correct (bool): Whether the submitted answer is correct.

        Returns:
            str: A formatted result string.
        """
        return "\n✓ CORRECT!" if is_correct else "\n✗ INCORRECT!"
    
    @staticmethod
    def format_session_end(score, total):
        """
        Formats the end-of-session display with the final score.

        Args:
            score (int): The user's final score.
            total (int): The total number of questions.

        Returns:
            str: A formatted session end string.
        """
        return f"\n{'='*50}\nSession completed!\nFinal Score: {score}/{total}\n{'='*50}"


class MenuHandler:
    """
    Handles the menu system and user interaction for the SAT Review System.
    """

    def __init__(self, session_factory):
        """
        Initializes the MenuHandler with a SessionFactory and DisplayFormatter.

        Args:
            session_factory (SessionFactory): An instance of SessionFactory for creating review sessions.
        """
        self.session_factory = session_factory
        self.formatter = DisplayFormatter()  
        
    def display_main_menu(self):
        """
        Displays the main menu and handles user input for section selection.

        Returns:
            str or None: The selected section type or None if the user chooses to exit.
        """
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
        """
        Displays the mode selection menu and handles user input.

        Returns:
            str or None: The selected mode ('simulation' or 'chill') or None if the user chooses to go back.
        """
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
        """
        Displays the question order menu for combined sections and handles user input.

        Returns:
            str or None: The selected order preference ('math_first' or 'reading_first') or None if the user chooses to go back.
        """
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
        """
        Converts the user's numeric choice to a section type string.

        Args:
            choice (str): The user's numeric choice ('1', '2', or '3').

        Returns:
            str: The corresponding section type ('math', 'reading', or 'combined').
        """
        return {
            '1': 'math',
            '2': 'reading',
            '3': 'combined'
        }[choice]
    
    def run(self):
        """
        Runs the main loop of the SAT Review System, handling user navigation through menus and sessions.
        """
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
        """
        Runs a chill review session, allowing users to navigate through questions at their own pace.

        Args:
            session (ChillSession): The chill review session to run.
        """
        print(self.formatter.format_header(f"Starting {session.session_type} chill review"))
        print(f"Total questions: {session.total_questions}")
        
        while True:
            question = session.get_current_question()
            if not question:
                break
            
            print(self.formatter.format_question(
                session.current_question_index + 1,
                session.total_questions,
                question.question_text
            ))
            
            # Display navigation options
            print("\nNavigation:")
            if session.current_question_index > 0:
                print("B - Go back to previous question")
            if session.current_question_index < session.total_questions - 1:
                print("N - Go to next question")
            print("A/B/C/D - Submit answer")
            print("Q - Quit session")
            
            # Display choices
            for letter, choice in question.choices.items():
                print(f"{letter}) {choice}")
            
            # Show previous answer if question was answered before
            if question.id in session.answers:
                previous_answer = session.answers[question.id]['user_answer']
                print(f"\nYour previous answer: {previous_answer}")
            
            answer = input("\nYour choice: ").upper()
            
            if answer == 'B' and session.current_question_index > 0:
                session.go_back()
                continue
            elif answer == 'N' and session.current_question_index < session.total_questions - 1:
                session.go_forward()
                continue
            elif answer == 'Q':
                break
            elif answer in ['A', 'B', 'C', 'D']:
                if question.id in session.answers:
                    is_correct = session.update_answer(answer)
                else:
                    is_correct = session.submit_answer(answer)
                
                print(self.formatter.format_result(is_correct))
                print(self.formatter.format_explanation(session.show_explanation()))
                
                input("\nPress Enter to continue...")
                session.answered_questions.add(question.id)
                
                if session.current_question_index < session.total_questions:
                    session.go_forward()
            else:
                print("Invalid input. Please try again.")
        
        print(self.formatter.format_session_end(session.score, session.total_questions))