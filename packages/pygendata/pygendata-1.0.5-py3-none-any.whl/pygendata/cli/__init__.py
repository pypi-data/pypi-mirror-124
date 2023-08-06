import argparse
import os
from pygendata import DataGenerator

parser = argparse.ArgumentParser(prog='pygendata', description='Python data generation library')

# Arguments
# generate: (csv, tsv, json)
# from: (ddl, tsv, json) <filepath>
# --rows (optional, default 100)
# to: (filepath to place results)
# pygendata --generate csv --base ddl /path/to/ddl --to /out/users.csv --rows 1000

parser.add_argument('--generate', type=str, help='The type of file to generate, options are csv, tsv, json')
parser.add_argument('--base', nargs=2, type=str, help='The type of file to generate data from, optons (ddl, json, tsv, csv) and the filepath where this file is located')
parser.add_argument('--template', nargs=2, help='The template to use to generate data (geo, medical, cellular ect..)')
parser.add_argument('--to', type=str, help='The filepath to place the results of the data generation in')
parser.add_argument('--rows', type=int, help='The number of rows to generate(default=100)')


def run():
    dg = None
    args = parser.parse_args()
    base_file_type = None
    base_file_loc = None
    template = None
    template_arg = None
    file_dest = args.to
    num_rows = args.rows
    filetype_to_generate = args.generate
    
    dg = DataGenerator(filetype_to_generate, rows=num_rows)
    if args.base:
        base_file_type, base_file_loc = args.base
    if args.template:
        template, template_arg = args.template
    
    filepath = os.getcwd()
    
    if base_file_type == 'ddl':
        dg.ddl(f"{filepath}/{base_file_loc}", f"{filepath}/{file_dest}") # this will need to be fixed when its used outside of this env
    elif template and template == 'geo':
        dg.template('geo', template_arg, f"{filepath}/{file_dest}")

if __name__ == "__main__":
    run()
