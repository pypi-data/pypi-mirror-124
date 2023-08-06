from subprocess import call
from .arg_parser import parse_arguments


def command_generator(account_feature_groups: list) -> str:
    """
    Use args, accounts, and features to construct behave command
    :param account_feature_groups:
    :return:
    """
    # get arguments
    args = parse_arguments()

    # get data for constructing behave command
    process_name = account_feature_groups[0][0]
    account = account_feature_groups[0][1].split()
    feature_set = account_feature_groups[1]

    # construct the behave command
    results_json = None
    commands = []
    for env in args.env:
        optional_retry = f'-D retry="{args.retry}" ' if args.retry > 1 else ' '
        optional_browser = f'-D browser="{args.browser}" -D headless="{args.headless}" ' if args.browser else ' '
        optional_userdata = f'-D user="{account[0]}" -D pass="{account[1]}" ' if args.account_file and args.account_section else ' '
        tags = f'--tags="{" and ".join(args.itags)} and ({" or ".join(feature_set)}){f"".join(" and not {}".format(t) for t in args.etags)}" '

        results_json = f'{args.output_dir}/{env}_process_{process_name}.json'

        project_specific_args = (' '.join([f"-D {arg}" for arg in args.arbitrary]) if args.arbitrary else ' ') + ' '

        cmd = (
                f'behave '
                f'-D parallel="True" ' +                # parallel
                f'-D env="{env}" ' +                    # environment
                optional_retry +                        # max number of tries
                optional_browser +                      # browser (basically always chrome)
                optional_userdata +                     # option user and password info
                tags +                                  # tags (include and exclude)
                project_specific_args +                 # vary based on project (easy to break)
                f'-f json.pretty -o {results_json} ' +  # formatter for results
                args.feature_dir                        # feature directory
        )
        commands.append(cmd)

    # run the command(s)
    for command in commands:
        # print(command); print()  # debug
        r = call(command, shell=True)

    return results_json
