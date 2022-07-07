from dotenv import load_dotenv
load_dotenv()

from website import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    # End program

