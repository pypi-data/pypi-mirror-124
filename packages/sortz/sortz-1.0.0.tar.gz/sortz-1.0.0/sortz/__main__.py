import argparse
import sys
from .visualizer import Visualizer
from .sorters import bubble_sort

def main():

    description = \
    f"""
A program to visualze various sorting algorithms.

example usage:
python {__file__} --sorter bubble --fps 30
    """

    parser = argparse.ArgumentParser(prog = f"python {__file__}", description = description,
                                     formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sorter", help = "sorting algorithm",
                        choices = ["bubble",], required = True)
    parser.add_argument("--fps", type = int, help = "fps of visualizer",
                        choices = range(1, 121), metavar = "{1-120}", required = True)

    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        sys.exit(1)
    args = parser.parse_args()

    sorter = None
    if args.sorter == "bubble":
        sorter = bubble_sort

    v = Visualizer(sorter, args.fps)
    v.main_loop()

if __name__ == "__main__":
    main()
