import os


def get_features(args, accounts) -> list:
    """
    Split the features as evenly as possible
    :param args:
    :param accounts:
    :return:
    """
    all_features = []

    for directory in os.walk(args.feature_dir):
        for file in directory[2]:
            if file.endswith('.feature'):
                all_features.append(f'@{args.board_name}.{file.split()[0]}')

    inc = -(-len(all_features) // args.processes)  # weird, yucky
    features = [all_features[i:i + inc] for i in range(0, len(all_features), inc)]
    return list(zip(accounts, features))
