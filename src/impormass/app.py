from .db.seed import init_schema
from .ui.login import run_login
from .ui.splash import run_splash


def main():
    init_schema()
    run_splash(run_login, duration_ms=3000)


if __name__ == "__main__":
    main()
