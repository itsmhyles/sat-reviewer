## SAT Review System

A comprehensive Python-based SAT practice system that offers both timed simulation and relaxed review modes for Math and Reading sections.

## Features

- **Multiple Study Modes**
  - Simulation Mode (Timed practice)
  - Chill Review Mode (Untimed practice)

- **Section Options**
  - Math Section
  - Reading and Writing Section
  - Combined Sections

- **Advanced Features**
  - Question randomization
  - Detailed explanations
  - Score tracking
  - Progress monitoring
  - Flexible session management

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sat-review-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required JSON files:
- Place `math_1.json` in the root directory
- Place `reading_1.json` in the root directory

## Project Structure

```
sat-review-system/
├── main.py
├── menu_handler.py
├── question_handler.py
├── session_manager.py
├── math_1.json
└── reading_1.json
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Navigate through the menus to:
- Select a section (Math/Reading/Combined)
- Choose a review mode (Simulation/Chill)
- For combined sections, select question order preference

3. Answer questions using A, B, C, or D

4. Review your performance after completing the session

## Question File Format

The JSON files should follow this structure:
```json
{
  "questions": [
    {
      "id": "unique_id",
      "question_text": "Question text",
      "choices": {
        "A": "First choice",
        "B": "Second choice",
        "C": "Third choice",
        "D": "Fourth choice"
      },
      "correct_answer": "A",
      "explanation": {
        "correct": "Explanation for correct answer",
        "incorrect": {
          "B": "Why B is wrong",
          "C": "Why C is wrong",
          "D": "Why D is wrong"
        }
      },
      "category": "topic",
      "difficulty": "medium"
    }
  ]
}
```

## System Requirements

- Python 3.7 or higher
- Text-based terminal/console
- Minimum 64MB RAM
- 10MB free disk space

