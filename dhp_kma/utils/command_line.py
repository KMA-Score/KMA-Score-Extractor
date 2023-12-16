import argparse


def create_command_line():
    parser = argparse.ArgumentParser(description='Process some integers.', prog="kma_score_dumper", epilog="From KMA "
                                                                                                           "with ❤️")

    dumper = parser.add_subparsers(dest='type')

    dumper_parser = dumper.add_parser('dump')
    dumper_parser.add_argument('path', type=str, metavar='path', help="Path to folder")
    dumper_parser.add_argument('--debug', '-d', action='store_true', help="Turn on debug mode")
    dumper_parser.add_argument('--output-path', '-o', metavar='output_path', action='store', help="Set csv output path")

    tool_parser = dumper.add_parser('tools')
    tool_sub_parser = tool_parser.add_subparsers(dest='tool_type')

    csv2json_parser = tool_sub_parser.add_parser('csv2json', help="Convert csv to json format", aliases=["c2j"])
    csv2json_parser.add_argument('input_path', type=str, metavar='input_path', help="CSV input path")
    csv2json_parser.add_argument('output_path', type=str, metavar='output_path', help="JSON output path")

    sql_gen_parser = tool_sub_parser.add_parser('sqlGenerate', help="Generate SQL command from csv",
                                                aliases=["sqlgen"])
    sql_gen_parser.add_argument('input_path', type=str, metavar='input_path', help="CSV input path")
    sql_gen_parser.add_argument('--output_path', '-o', type=str, metavar='output_path', help="SQL output path",
                                required=False)

    args = parser.parse_args()

    return args, parser
