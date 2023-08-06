from argparse import ArgumentParser
from sys import stdout

from boto3.session import Session

from stackdiff.stack_diff import StackDiff
from stackdiff.version import get_version


def cli_entry() -> None:
    parser = ArgumentParser(
        description="Visualises the changes described by an Amazon Web Services CloudFormation stack change set.",
        epilog="Made with love by Cariad Eccleston: https://github.com/cariad/stackdiff",
    )

    parser.add_argument("--change", help="change set ARN, ID or name")
    parser.add_argument("--stack", help="stack ARN, ID or name")
    parser.add_argument("--version", action="store_true", help="print the version")

    args = parser.parse_args()

    if args.version:
        print(get_version())
        exit(0)

    cs = StackDiff(change=args.change, session=Session(), stack=args.stack)
    cs.render_differences(stdout)
    cs.render_changes(stdout)


if __name__ == "__main__":
    cli_entry()
