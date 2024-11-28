from session_manager import SessionFactory
from menu_handler import MenuHandler

def main():
    session_factory = SessionFactory()
    menu = MenuHandler(session_factory)
    menu.run()

if __name__ == "__main__":
    main()