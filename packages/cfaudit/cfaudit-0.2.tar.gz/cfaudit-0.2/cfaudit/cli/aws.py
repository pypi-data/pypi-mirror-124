
import click
import cfaudit


AWS_AVAILABLE_OUTPUT_OPTIONS = [
    'human',
    'json',
    'yml',
]


@click.command(
    'analyze',
    help="Generate the analysis output"
)
@click.option(
    '-r', '--region',
    'region',
    required=True,
    help='AWS Region to list the security groups',
    metavar='<region_id>',
)
@click.option(
    '-p', '--profile',
    'profile',
    help='AWS CLI configured profile which will be used',
    metavar='<profile_name>',
)
@click.option(
    '-o', '--output',
    'output',
    default='human',
    help='Which kind of output you want the analysis',
    type=click.Choice(AWS_AVAILABLE_OUTPUT_OPTIONS),
)
@click.option(
    '--whitelist',
    'whitelist_path',
    help='Path to whitelist with declared safe IPs and CIDR',
    metavar='<path>',
)
def aws_analyze_command(region, profile, output, whitelist_path):
    """
    This function is called when the user types
    "cfaudit aws analyze"
    """
    aws_output_options = {
        "human": cfaudit.aws.output.print_human,
        "json": cfaudit.generic.output.print_json,
        "yml": cfaudit.generic.output.print_yml,
    }

    if whitelist_path:
        whitelist = cfaudit.generic.helpers.parse_whitelist_file(
            whitelist_path=whitelist_path
        )
    else:
        whitelist = []

    session = cfaudit.aws.authentication.create_session(
        region=region,
        profile=profile,
    )

    if session:
        analysis = cfaudit.aws.analysis.analyze_security_groups(
            session=session,
            whitelist=whitelist,
        )
        print(aws_output_options.get(output)(analysis=analysis))


if __name__ == "__main__":
    pass
