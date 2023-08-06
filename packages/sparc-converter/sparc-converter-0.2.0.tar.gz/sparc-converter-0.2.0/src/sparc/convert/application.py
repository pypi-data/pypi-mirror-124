import argparse
import os.path
import sys

from opencmiss.exporter.webgl import ArgonSceneExporter


def process_arguments():
    parser = argparse.ArgumentParser(description="Convert SPARC data.")
    subparsers = parser.add_subparsers(help='Choose a command', dest='command_name')
    subparsers.required = True
    web_gl_parser = subparsers.add_parser('web-gl', help='export to WebGL')
    web_gl_parser.set_defaults(action=lambda: 'web-gl')
    web_gl_parser.add_argument('-p', '--prefix', help='set web-gl output prefix')
    web_gl_parser.add_argument('argon_doc', help='an Argon document')

    parser.add_argument('-o', '--output-dir', default='.',
                        help='specify the output directory')

    return parser


def main():
    parser = process_arguments()
    args = parser.parse_args()

    if not os.path.isfile(args.argon_doc):
        sys.exit(1)

    if args.command_name == 'web-gl':
        exporter = ArgonSceneExporter(args.output_dir, args.prefix)
        exporter.load(args.argon_doc)
        exporter.export()
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
