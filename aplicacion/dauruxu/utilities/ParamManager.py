import argparse


def create_settings_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings-path', '-s', type=str, required=True)
    return parser
