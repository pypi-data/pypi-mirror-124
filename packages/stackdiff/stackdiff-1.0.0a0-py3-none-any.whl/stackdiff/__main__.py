from argparse import ArgumentParser
from sys import stdout

from boto3.session import Session

from stackdiff.version import get_version
from stackdiff.change_set import StackDiff


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

    # runtime_args = vars(args)
    # if unknown:
    #     runtime_args["args"].extend(unknown)

    # command_type = commands.get(args.command)
    # config_path = Path(args.config_path)
    # config = Configuration(
    #     config_dir=config_path,
    #     runtime_args=runtime_args["args"],
    # ).load()

    # if args.password_stdin:
    #     # Authenticate via stdin now to get and save a refresh token for later:
    #     auth_result = Authenticate.make_via_config_opts(
    #         config=config,
    #         password_options={"password": None, "prompt_via_stdin": True},
    #     ).execute()
    #     if not auth_result.succeeded:
    #         print_command_execution_result(auth_result)
    #         exit(1)

    # command = command_type.make_via_config(config=config)

    # result = command.execute()
    # print_command_execution_result(result)
    # exit(0 if result.succeeded else 1)


if __name__ == "__main__":
    cli_entry()
