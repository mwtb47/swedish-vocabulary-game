"""Script to run the translation game.

This script runs the translation game with the option of not committing
the marks to the database at the end of the game.

Arguments:
    --no-commit: Do not commit marks to database.

Functions:
    main: Initiate Game class and run the game.
"""

import argparse

import app


def main() -> None:
    """Run translation game."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-commit",
        default=False,
        action="store_true",
        help="Do not commit marks to database.",
    )
    args = parser.parse_args()

    game = app.Game(args.no_commit)
    game.run()
    game.commit_marks()


if __name__ == "__main__":
    main()
