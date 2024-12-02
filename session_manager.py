# session_manager.py
from question_handler import QuestionBank, QuestionManager
import time
from datetime import datetime, timedelta

class BaseSession:
    """
    Base class for managing a question session.

    This class provides the fundamental structure for both simulation and chill sessions.

    Attributes:
        questions (list): List of Question objects for the session.
        session_type (str): Type of the session ('math', 'reading', or 'combined').
        current_question_index (int): Index of the current question.
        answers (dict): Dictionary to store user answers and their correctness.
        score (int): Current score of the user.
        total_questions (int): Total number of questions in the session.
    """

    def __init__(self, questions, session_type):
        self.questions = questions
        self.session_type = session_type
        self.current_question_index = 0
        self.answers = {}
        self.score = 0
        self.total_questions = len(questions)
    
    def get_current_question(self):
        """
        Retrieves the current question in the session.

        Returns:
            Question: The current question object, or None if all questions have been answered.
        """
        if self.current_question_index < self.total_questions:
            return self.questions[self.current_question_index]
        return None
    

    def submit_answer(self, answer):
        
        """
        Submits an answer for the current question and updates the session state.

        Args:
            answer (str): The user's answer to the current question.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """

        if self.current_question_index >= self.total_questions:
            return False

        question = self.questions[self.current_question_index]
        is_correct = answer.upper() == question.correct_answer
        self.answers[question.id] = {
            'user_answer': answer,
            'correct': is_correct,
            'question_text': question.question_text
        }

        if is_correct:
            self.score += 1

        self.current_question_index += 1  # Increment to move to the next question
        return is_correct


class SimulationSession(BaseSession):
    """
    A session class for timed simulations.

    This class extends BaseSession to include timing functionality for simulation sessions.

    Attributes:
        time_limit (int): Time limit for the session in minutes.
        start_time (float): Timestamp when the session started.
        end_time (float): Timestamp when the session should end.
        is_active (bool): Flag indicating if the session is currently active.
    """

    def __init__(self, questions, session_type):
        super().__init__(questions, session_type)
        self.time_limit = 60 if session_type == 'combined' else 30
        self.start_time = None
        self.end_time = None
        self.is_active = False
    
    def start_session(self):
        """
        Starts the simulation session and sets the start and end times.

        Returns:
            bool: Always returns True to indicate successful start.
        """
        self.start_time = time.time()
        self.end_time = self.start_time + (self.time_limit * 60)
        self.is_active = True
        return True
    
    def get_remaining_time(self):
        """
        Calculates the remaining time in the session.

        Returns:
            float: The remaining time in seconds, or the full time limit if the session hasn't started.
        """
        if not self.start_time:
            return self.time_limit * 60
        remaining = self.end_time - time.time()
        return max(0, remaining)

    def format_time_remaining(self):
        """
        Formats the remaining time as a string.

        Returns:
            str: The remaining time formatted as "MM:SS".
        """
        remaining = self.get_remaining_time()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def is_time_up(self):
        """
        Checks if the session time has expired.

        Returns:
            bool: True if the time is up, False otherwise.
        """
        return self.get_remaining_time() <= 0


class ChillSession(BaseSession):
    
    """
    A session class for relaxed, untimed practice.

    This class extends BaseSession to include functionality specific to chill sessions.

    Attributes:
        review_mode (bool): Indicates whether the session is in review mode.
    """
    def __init__(self, questions, session_type):
        super().__init__(questions, session_type)
        self.review_mode = True
        self.answered_questions = set()
        self.current_explanation = None  # Track current explanation


    def go_back(self):
        """Go back to the previous question if possible"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            return True
        return False
    
    def go_forward(self):
        """Go forward to the next question if possible"""
        if self.current_question_index < self.total_questions - 1:
            self.current_question_index += 1
            return True
        return False
    
    def update_answer(self, answer):
        """Update an existing answer and recalculate score"""
        question = self.questions[self.current_question_index]
        old_answer = self.answers.get(question.id)
        
        # Remove point for previous correct answer
        if old_answer and old_answer['correct']:
            self.score -= 1
        
        # Check new answer
        is_correct = answer.upper() == question.correct_answer
        if is_correct:
            self.score += 1
        
        # Update answer in dictionary
        self.answers[question.id] = {
            'user_answer': answer,
            'correct': is_correct,
            'question_text': question.question_text
        }
        
        return is_correct
    
    def show_explanation(self):
        """
        Retrieves the explanation for the current question.
        Returns:
            dict: The explanation for the current question
        """
        if self.current_question_index < self.total_questions:
            # Get the current question's explanation, not the next one
            current_question = self.questions[self.current_question_index]
            return current_question.explanation
        return None

    def _format_explanation(self, explanation):
        """
        Formats the explanation in a more aesthetic manner.

        Expected:
        Correct Answer Explanation:
        [explanation for the correct answer]

        Why other answers are incorrect:

        Choice B: [explanation for why B is incorrect]

        """
        formatted_text = "\nCorrect Answer Explanation:\n"
        formatted_text += explanation['correct'] + "\n"
        
        if 'incorrect' in explanation:
            formatted_text += "\nWhy other answers are incorrect:\n"
            for choice, reason in explanation['incorrect'].items():
                formatted_text += f"\nChoice {choice}: {reason}"
        
        return formatted_text


class SessionFactory:
    """
    Factory class for creating different types of sessions.

    This class manages the creation of simulation and chill sessions, utilizing the QuestionBank
    and QuestionManager from the question_handler module.

    Attributes:
        question_bank (QuestionBank): The question bank containing all available questions.
        manager (QuestionManager): The question manager for handling question selection.
    """

    def __init__(self):
        self.question_bank = QuestionBank()
        self.question_bank.load_questions('math_1.json', 'math')
        self.question_bank.load_questions('reading_1.json', 'reading')
        self.manager = QuestionManager(self.question_bank)
    
   
    def create_session(self, section_type, mode, question_count=None, order_preference=None):
        """
        Creates a new session based on the specified parameters.

        Args:
            section_type (str): The type of session ('math', 'reading', or 'combined').
            mode (str): The mode of the session ('simulation' or 'chill').
            question_count (int, optional): The number of questions for the session.

        Returns:
            BaseSession: An instance of either SimulationSession or ChillSession.
        """
        # Validate inputs
        if section_type not in ['math', 'reading', 'combined']:
            raise ValueError("Invalid section type. Must be 'math', 'reading', or 'combined'")
        if mode not in ['simulation', 'chill']:
            raise ValueError("Invalid mode. Must be 'simulation' or 'chill'")
        
        # Set default question count based on mode and section
        if mode == 'simulation':
            question_count = 50 if section_type == 'combined' else 25
        else:
            question_count = 20
        
        # Get appropriate questions
        if section_type == 'combined':
            math_qs = self.manager.get_questions_by_section('math')
            reading_qs = self.manager.get_questions_by_section('reading')
            
            # Handle combined questions based on order preference
            if order_preference == 'math_first':
                questions = (self.manager.shuffle_questions(math_qs, count=question_count//2) + 
                            self.manager.shuffle_questions(reading_qs, count=question_count//2))
            else:
                questions = (self.manager.shuffle_questions(reading_qs, count=question_count//2) + 
                            self.manager.shuffle_questions(math_qs, count=question_count//2))
        else:
            questions = self.manager.get_questions_by_section(section_type)
            questions = self.manager.shuffle_questions(questions, count=question_count)
        
        # Create and return appropriate session type
        if mode == 'simulation':
            return SimulationSession(questions, section_type)
        return ChillSession(questions, section_type)

class TimerDisplay:
    """
    Handles the display of the timer for simulation sessions.

    This class provides methods to display and clear the timer on the console.

    Attributes:
        session (SimulationSession): The simulation session to display the timer for.
    """

    def __init__(self, session):
        self.session = session
    
    def display_timer(self):
        """
        Displays the current remaining time on the console.
        """
        if self.session.is_active:
            time_str = self.session.format_time_remaining()
            print(f"\rTime Remaining: {time_str}", end="", flush=True)
    
    def clear_timer(self):
        """
        Clears the timer display from the console.
        """
        print("\r" + " " * 30 + "\r", end="", flush=True)



def run_simulation_session(questions, session_type):
    """
    Runs a complete simulation session.

    This function creates a simulation session, manages the timer display, and handles
    the flow of questions and answers until the session is complete.

    Args:
        questions (list): List of Question objects for the session.
        session_type (str): Type of the session ('math', 'reading', or 'combined').
    """
    session = SimulationSession(questions, session_type)
    timer = TimerDisplay(session)
    
    print(f"\nStarting {session_type} simulation - {session.time_limit} minutes")
    print(f"Total questions: {session.total_questions}")
    session.start_session()
    
    while not session.is_time_up():
        timer.display_timer()
        current_question = session.get_current_question()
        if not current_question:
            print("\nAll questions completed!")
            break
        
        print(f"\nQuestion {session.current_question_index + 1} of {session.total_questions}")
        current_question.display()
        
        answer = input("\nYour answer (A/B/C/D): ").upper()
        while answer not in ['A', 'B', 'C', 'D']:
            print("Invalid input. Please enter A, B, C, or D.")
            answer = input("Your answer (A/B/C/D): ").upper()
        
        timer.clear_timer()
        
        if session.is_time_up():
            print("\nTime's up!")
            break
        
        session.submit_answer(answer)
    
    # Display final score and review section
    print("\n" + "="*50)
    print(f"Session completed!\nFinal Score: {session.score}/{session.total_questions}")
    print(f"Percentage: {(session.score/session.total_questions)*100:.2f}%")
    print("="*50)
    
    # Review section
    print("\nWould you like to review your answers? (Y/N)")
    if input().upper() == 'Y':
        print("\n=== Review Session ===")
        for i, question in enumerate(questions):
            if question.id in session.answers:
                answer = session.answers[question.id]
                print(f"\nQuestion {i+1}:")
                print(question.question_text)
                print("\nYour answer:", answer['user_answer'])
                print("Correct answer:", question.correct_answer)
                print("✓ Correct!" if answer['correct'] else "✗ Incorrect!")
                
                if not answer['correct']:
                    print("\nExplanation:")
                    print("-"*50)
                    print("Correct Answer Explanation:")
                    print(question.explanation['correct'])
                    print("\nWhy your answer was incorrect:")
                    if answer['user_answer'] in question.explanation['incorrect']:
                        print(question.explanation['incorrect'][answer['user_answer']])
                
                input("\nPress Enter for next question...")