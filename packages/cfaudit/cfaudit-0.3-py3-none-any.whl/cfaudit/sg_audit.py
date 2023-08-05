#!/usr/bin/env python
import click
import pkg_resources
import cfaudit.cli.aws


@click.group()
def main():
    """AWS SG Audit
    """
    pass


@main.group(
    'aws',
    help='Amazon Web Services'
)
def aws_group():
    pass


"""
Adding commands to Click Groups
"""
aws_group.add_command(cfaudit.cli.aws.aws_analyze_command)


if __name__ == "__main__":
    main()
    exit()
