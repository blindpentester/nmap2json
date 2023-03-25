#!/bin/python3

from collections import defaultdict
import sys
import json
import argparse
from lxml import etree

def main():
    parser = argparse.ArgumentParser(description='Convert nmap, or any XML output to JSON format.')
    parser.add_argument('-o', '--output', help='Output file name', required=False, nargs='?')
    args = parser.parse_args()

    if args.output is None:
        parser.print_help()
        sys.exit(1)

    try:
        if not sys.stdin.isatty():
            if args.output == '-':
                output = sys.stdout
            else:
                output = open(args.output, 'a')
            with output:
                output.write('[\n')

                context = etree.iterparse(sys.stdin.buffer, events=('end',), tag='host')

                first = True
                for event, elem in context:
                    host_dict = etree.tostring(elem, encoding='unicode', method='xml')
                    host_json = xml_to_json(host_dict)

                    if not first:
                        output.write(',\n')
                    else:
                        first = False

                    output.write(host_json)

                    # Clear the element to free memory
                    elem.clear()
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]

                output.write('\n]')

                if args.output != '-':
                    print(f"JSON output saved to {args.output}")
        else:
            print("Usage:")
            print("  nmap [OPTIONS] [TARGET] -oX - | ./XML-to-JSONu.py -o output.json")
            print("  cat <filename>.xml | ./XML-to-JSON.py -o <outputfile>.json")
            sys.exit(1)
    except Exception as e:
        print(f"Error processing XML file: {e}")
        sys.exit(1)

def xml_to_json(xml_data):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_data, parser)
        python_dict = etree_to_dict(root)
        json_data = json.dumps(python_dict, indent=4)
        return json_data
    except Exception as e:
        print(f"Error converting XML to JSON: {e}")
        sys.exit(1)

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

if __name__ == "__main__":
    main()
