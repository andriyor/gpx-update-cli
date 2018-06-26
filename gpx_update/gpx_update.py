import datetime
import os

import gpxpy.gpx
import click
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


@click.command()
@click.argument('input-file-path', type=click.Path(exists=True),)
@click.option('--new-time', default=datetime.datetime.now(),
              help='specify date and time for all point current date by default')
@click.option('--new', 'ofn', flag_value='new', default=True, help='output file name with e.x old_name_new by default')
@click.option('--ow', 'ofn', flag_value='rewrite', help='overwrite a file')
@click.option('--ui', 'ofn', flag_value='user-input', help='specify output file name manually')
def cli(input_file_path, new_time, ofn):
    if not isinstance(new_time, datetime.datetime):
        new_time = parse(new_time)

    gpx_file = open(input_file_path, 'r')
    gpx = gpxpy.parse(gpx_file)
    delta = relativedelta(new_time, gpx.time)
    gpx.adjust_time(delta)

    if ofn == 'new':
        filename_w_ext = os.path.basename(input_file_path)
        filename, file_extension = os.path.splitext(filename_w_ext)
        filename = '{}_new.gpx'.format(filename)
    elif ofn == 'ow':
        filename = input_file_path
    elif ofn == 'user-input':
        filename = click.prompt('Please enter a new file name')
        filename = '{}.gpx'.format(filename)

    with open(filename, 'w') as f:
        f.write(gpx.to_xml())
