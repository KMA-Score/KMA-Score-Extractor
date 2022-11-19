import argparse


def create_command_line():
    parser = argparse.ArgumentParser(description='Process some integers.', prog="kma_score_dumper", epilog="From KMA "
                                                                                                           "with ❤️")

    dumper = parser.add_subparsers(dest='type')

    dumper_parser = dumper.add_parser('dump')
    dumper_parser.add_argument('path', type=str, metavar='path')
    dumper_parser.add_argument('--debug', '-d', action='store_true')
    dumper_parser.add_argument('--output-path', metavar='output_path', action='store')

    tool_parser = dumper.add_parser('tool')
    tool_parser.add_argument('path', type=str, metavar='path')
    tool_parser.add_argument('--debug', '-d', action='store_true')

    args = parser.parse_args()

    return args, parser
