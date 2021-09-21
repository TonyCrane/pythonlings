import argparse
import sys
import os
from .exercise import read_exercises, State
from .run import run, verify
from .watch import watch

VERSION = "0.0.1"

def get_parser():
    parser = argparse.ArgumentParser(
        description="Pythonlings is a collection of small exercises to get you used to writing and reading Python code",
        prog="pythonlings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""commands:
  verify            Verifies all exercises according to the recommended order
  watch             Reruns `verify` when files were edited
  run {exercise}    Runs a single exercise
  hint {exercise}   Returns a hint for the given exercise
  list              Lists the exercises available in Rustlings\n"""
    )
    parser.add_argument(
        'command', nargs="*",
        help='the commend you want to execute'
    )
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="show the executable version"
    )
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        print(f"\033[1;32mPythonlings v{VERSION}\033[0m")
    
    if not args.command:
        if args.version:
            sys.exit(0)
        else:
            print("")
            print("                 welcome to...                           ")
            print("              _   _                 _ _                  ")
            print("  _ __  _   _| |_| |__   ___  _ __ | (_)_ __   __ _ ___  ")
            print(" | '_ \| | | | __| '_ \ / _ \| '_ \| | | '_ \ / _` / __| ")
            print(" | |_) | |_| | |_| | | | (_) | | | | | | | | | (_| \__ \ ")
            print(" | .__/ \__, |\__|_| |_|\___/|_| |_|_|_|_| |_|\__, |___/ ")
            print(" |_|    |___/                                 |___/      ")
            print("")
            parser.print_help()
            sys.exit(0)

    if not os.path.exists("info.yml"):
        print("pythonlings must be run from the `pythonlings/` directory!")
        sys.exit(1)
    
    exercises = read_exercises("info.yml")

    if args.command[0] == "verify":
        verify(exercises)
    elif args.command[0] == "watch":
        watch(exercises)
    elif args.command[0] == "run":
        if len(args.command) == 1:
            print("\033[31mRequired exercise name arguments not provided\033[0m")
            print("You are supposed to run an exercises like `pythonlings run variables1` or `pythonlings run next`")
            sys.exit(1)
        exercise = find_exercise(args.command[1], exercises)
        run(exercise)
    elif args.command[0] == "hint":
        if len(args.command) == 1:
            print("\033[31mRequired exercise name arguments not provided\033[0m")
            print("You are supposed to get hints like `pythonlings hint variables1`")
            sys.exit(1)
        exercise = find_exercise(args.command[1], exercises)
        print(exercise.hint)
    elif args.command[0] == "list":
        list_exercises(exercises)
    else:
        print(f"\033[31mUnrecognized argument: {args.command[0]}\033[0m")
        parser.print_help()
        sys.exit(1)


def find_exercise(name, exercises):
    if name == "next":
        for exercise in exercises:
            if exercise.state == State.NOTDONE:
                return exercise
        print("🎉 Congratulations! You have done all the exercises!")
        print("🔚 There are no more exercises to do next!")
        sys.exit(0)
    else:
        for exercise in exercises:
            if exercise.name == name:
                return exercise
        print(f"\033[31mNo exercise found for '{exercise.name}'!\033[0m")
        sys.exit(1)


def list_exercises(exercises):
    print("Listing exercises...(must remove \"I AM NOT DONE\" comment to indicate as done)\n")
    print("{:<17}\t{:<46}\t{:<8}".format("Name", "Path", "Status"));
    result = []
    done_cnt = 0
    for exercise in exercises:
        exercise.check_state()
        if exercise.state == State.DONE:
            done_cnt += 1
            result.append(
                "\033[32m{:<17}\t{:<46}\t{:<8}\033[0m".format(
                    exercise.name, exercise.path, "Done"
                )
            )
        else:
            result.append(
                "\033[31m{:<17}\t{:<46}\t{:<8}\033[0m".format(
                    exercise.name, exercise.path, "Not done"
                )
            )
    print("\n".join(result))
    print(
        "\nProgress: You completed {} / {} exercises ({:.2f} %).".format(
            done_cnt,
            len(exercises),
            100.0 * done_cnt / len(exercises)
        )
    )



if __name__ == "__main__":
    main()