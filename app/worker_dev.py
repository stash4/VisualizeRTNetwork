from os.path import join, dirname
from dotenv import load_dotenv
from . import worker


def main():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    worker.main()


if __name__ == '__main__':
    main()
