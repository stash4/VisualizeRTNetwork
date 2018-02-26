from os.path import join, dirname
from dotenv import load_dotenv
from app import app


def main():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()
