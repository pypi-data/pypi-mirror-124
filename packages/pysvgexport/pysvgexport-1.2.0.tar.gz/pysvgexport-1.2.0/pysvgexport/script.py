#!/usr/bin/python3
import argparse
import sys

from pysvgexport import SVGExport


def main():
    try:
        parser = argparse.ArgumentParser(description='Welcome to SVG Exporter')
        required = parser.add_argument_group('required arguments')
        required.add_argument('-f', '--file', nargs='?', help='(Required) SVG file path to export.', required=True)
        required.add_argument('-s', '--scale', nargs='?', help='(Required) Scale ratio for output file.', required=True)
        parser.add_argument('-o', '--output', nargs='?', help='(Optional) Output image path to save.')
        parser.add_argument('-t', '--transparent', nargs='?', help='(Optional) Omit background or not.')
        parser.add_argument('-w', '--statics', nargs='?',
                            help='(Optional) Static file url list (font,...) in this svg. Format: url1,url2,url3,...')

        groups_order = {
            'positional arguments': 0,
            'required arguments': 1,
            'optional arguments': 2
        }
        parser._action_groups.sort(key=lambda g: groups_order[g.title])
        args = parser.parse_args()

        file_path = args.file
        print(f"Read SVG file {file_path}")
        with open(file_path) as file:
            svg_data = " ".join([line.rstrip() for line in file])

        static_url_list = args.statics.split(',') if args.statics else []
        capture_options = {"scale": int(args.scale), "static_url_list": static_url_list}
        output_options = {"omitBackground": args.transparent or True}

        if args.output:
            output_path = args.output
        else:
            output_path = file_path.replace('svg', 'png')

        oqs = SVGExport(svg_data=svg_data, capture_options=capture_options, output_options=output_options)
        image = oqs.execute()
        image.save(output_path, format="PNG")
        print(f"Export SVG successfully to {output_path}")

    except argparse.ArgumentError:
        print('Wrong syntax')
        print('Please run "svgexport -h" to see the usage')
        sys.exit(2)
