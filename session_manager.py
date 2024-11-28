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
        
        self.current_question_index += 1
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
    
    def show_explanation(self):
        """
        Retrieves the explanation for the previous question.

        Returns:
            str: The explanation for the previous question, or None if at the first question.
        """
        if self.current_question_index > 0:
            previous_question = self.questions[self.current_question_index - 1]
            return previous_question.explanation


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
    
    def create_session(self, section_type, mode, question_count=None):
        """
        Creates a new session based on the specified parameters.
        """
        # Validate inputs
        if section_type not in ['math', 'reading', 'combined']:
            raise ValueError("Invalid section type. Must be 'math', 'reading', or 'combined'")
        if mode not in ['simulation', 'chill']:
            raise ValueError("Invalid mode. Must be 'simulation' or 'chill'")
        
        # Set default question count based on mode
        if question_count is None:
            question_count = 25 if mode == 'simulation' else 10

        # Get appropriate questions
        if section_type == 'combined':
            math_qs = self.manager.get_questions_by_section('math')
            reading_qs = self.manager.get_questions_by_section('reading')
            questions = self.manager.shuffle_questions(math_qs + reading_qs, count=question_count)
        else:
            questions = self.manager.get_questions_by_section(section_type)
            questions = self.manager.shuffle_questions(questions, count=question_count)
        
        # Validate questions
        if not questions:
            raise ValueError(f"No questions available for {section_type} section")
        if len(questions) < question_count:
            raise ValueError(f"Not enough questions available. Requested {question_count}, but only {len(questions)} available")

        # Create and return appropriate session type
        if mode == 'simulation':
            return SimulationSession(questions, section_type)
        return ChillSession(questions, section_type)
    

def create_session(self, section_type, mode, question_count=None):
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
    
    # Set default question count based on mode
    if question_count is None:
        question_count = 25 if mode == 'simulation' else 10

    # Get appropriate questions
    if section_type == 'combined':
        math_qs = self.manager.get_questions_by_section('math')
        reading_qs = self.manager.get_questions_by_section('reading')
        questions = self.manager.shuffle_questions(math_qs + reading_qs, count=question_count)
    else:
        questions = self.manager.get_questions_by_section(section_type)
        questions = self.manager.shuffle_questions(questions, count=question_count)
    
    # Validate questions
    if not questions:
        raise ValueError(f"No questions available for {section_type} section")
    if len(questions) < question_count:
        raise ValueError(f"Not enough questions available. Requested {question_count}, but only {len(questions)} available")

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

