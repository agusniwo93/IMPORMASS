from .db.seed import init_schema
from .ui.login import run_login

def main():
    init_schema()
    run_login()

if __name__ == "__main__":
    main()
