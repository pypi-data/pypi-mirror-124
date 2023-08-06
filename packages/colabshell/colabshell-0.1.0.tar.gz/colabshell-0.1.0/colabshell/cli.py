#! /usr/bin/env python
import sys
import argparse
from colabshell import ColabShell


def main():
    parser = argparse.ArgumentParser(
        description="ColabShell: Run Shell On Colab/Kaggle Notebooks"
    )
    parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    required.add_argument(
        "port",
        type=int,
        help="the port you want to run ttyd server on",
        required=True,
    )
    optional.add_argument(
        "interactive",
        action="store_true",
        required=False,
        default=False
    )
    optional.add_argument(
        "--credential",
        type=str,
        help="username and password to protect your shell from unauthorized access, format username:password",
        default=None,
    )
    
    optional.add_argument(
        "--mount_drive",
        action="store",
        required=False,
        default=None,
        nargs=1,
        help="if you pass path to --mount_drive, your google drive will be mounted",
    )
    optional.add_argument(
        "--logger_name",
        type=str, default="colab.kafka", help="default logger name"
    )
    optional.add_argument(
        "--settings_ini", 
        type=str, default=None, help="Settings ini to load the initial configuration kafka logger"
    )

    args = parser.parse_args()
    if args.credential and len(args.credential.split(":")) != 2:
        print("Invalid credentail pair, should be in username:password format")
        sys.exit(1)
    
    try:
        username, password = args.credential.split(":")
        shell = ColabShell(
            port=args.port,
            username=username, 
            password=password, 
            mount_drive=args.mount_drive,
            interactive=args.interactive,
            logger_name=args.logger_name, 
            settings_ini=args.settings_ini,
        )
        shell.run()
    except KeyboardInterrupt:
        print("Closing .....")


if __name__ == "__main__":
    main()
