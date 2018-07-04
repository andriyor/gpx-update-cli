import datetime
import collections
import os
import configparser

from stravaweblib import WebClient, DataFormat
import gpxpy.gpx
import click
from halo import Halo
from pick import pick
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from units import unit
from units.predefined import define_units


def get_config_path():
    return os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.join(os.environ['HOME'], '.config')), 'strava-relive.ini')


def get_label(activity):
    return ', '.join(map(str, [activity.start_date_local, activity.name, activity.moving_time, activity.distance,
                               activity.total_elevation_gain]))


@Halo(text='Updating GPX file', spinner='dots')
def process_and_save(input_file_path, new_time, new_filename):
    gpx_file = open(input_file_path, 'r')
    gpx = gpxpy.parse(gpx_file)
    delta = relativedelta(new_time, gpx.time)
    gpx.adjust_time(delta)

    with open(new_filename, 'w') as f:
        f.write(gpx.to_xml())


@Halo(text='Fetch activity from Strava', spinner='dots')
def fetch_and_save(client, id):
    data = client.get_activity_data(id, fmt=DataFormat.GPX)
    with open(data.filename, 'wb') as f:
        for chunk in data.content:
            f.write(chunk)
    return data.filename


def update_activity(client, id, new_time):
    filename = fetch_and_save(client, id)
    process_and_save(filename, new_time, filename)
    with Halo(text='Upload activity to Strava', spinner='dots'):
        client.upload_activity(activity_file=open(filename, 'r'), data_type='gpx')


@click.group(chain=True)
@click.option('--new-time', default=datetime.datetime.now(), help='specify date and time for all point current date by default')
@click.pass_context
def cli(ctx, new_time):
    """Updating GPX dates"""
    if not isinstance(new_time, datetime.datetime):
        new_time = parse(new_time)
    ctx.obj = {'new_time': new_time}


@cli.command('file')
@click.argument('input-file-path', type=click.Path(exists=True))
@click.option('--new', 'ofn', flag_value='new', default=True, help='output file name with e.x old_name_new by default')
@click.option('--ow', 'ofn', flag_value='rewrite', help='overwrite a file')
@click.option('--ui', 'ofn', flag_value='user-input', help='specify output file name manually')
@click.pass_context
def file(ctx, input_file_path, ofn):
    """Create updated GPX file"""
    new_time = ctx.obj['new_time']

    if ofn == 'new':
        filename_w_ext = os.path.basename(input_file_path)
        filename, file_extension = os.path.splitext(filename_w_ext)
        new_filename = '{}_new.gpx'.format(filename)
    elif ofn == 'ow':
        new_filename = input_file_path
    elif ofn == 'user-input':
        filename = click.prompt('Please enter a new file name')
        new_filename = '{}.gpx'.format(filename)

    process_and_save(input_file_path, new_time, new_filename)


@cli.command()
@click.option('--config-file', envvar='RIOD_CONFIG_FILE', default=get_config_path())
@click.option('--delete/--no-delete', default=False)
@click.pass_context
def strava(ctx, config_file, delete):
    """Login to Strava account"""
    ctx.obj['delete'] = delete

    config = configparser.ConfigParser()
    config.read(config_file)

    api_token = config.get('global', 'api_token')
    email = config.get('user', 'email')
    password = config.get('user', 'password')

    with Halo(text='Login', spinner='dots'):
        client = WebClient(access_token=api_token, email=email, password=password)
        ctx.obj['client'] = client


@cli.command('id')
@click.argument('id')
@click.pass_context
def strava_id(ctx, id):
    """Getting GPX file by activity id and upload to Strava"""
    new_time = ctx.obj['new_time']
    client = ctx.obj['client']

    update_activity(client, id, new_time)


@cli.command('sfile')
@click.argument('input-file-path', type=click.Path(exists=True))
@click.pass_context
def strava_file(ctx, input_file_path):
    """Updating GPX file from and upload to Strava"""
    new_time = ctx.obj['new_time']
    client = ctx.obj['client']

    process_and_save(input_file_path, new_time, input_file_path)
    with Halo(text='Upload activity to Strava', spinner='dots'):
        client.upload_activity(activity_file=open(input_file_path, 'r'), data_type='gpx')


@cli.command('pick')
@click.option('--before', help='Result will start with activities whose start date is before specified date. (UTC)')
@click.option('--after', help='Result will start with activities whose start date is after specified value. (UTC)')
@click.option('--limit', default=10, help='How many maximum activities to return.')
@click.pass_context
def strava_pick(ctx, limit, before, after):
    """Getting GPX file by picked activity and upload to Strava"""
    new_time = ctx.obj['new_time']
    client = ctx.obj['client']

    define_units()
    kilometers = unit('km')

    activities = []
    Activity = collections.namedtuple('Activity', ['id', 'start_date_local', 'name', 'moving_time', 'distance',
                                                   'total_elevation_gain'])

    with Halo(text='Fetch activities from Strava', spinner='dots'):
        fetched_activities = client.get_activities(before, after, limit)

    for activity in fetched_activities:
        activities.append(Activity(id=activity.id, start_date_local=activity.start_date_local, name=activity.name,
                                   moving_time=activity.moving_time, distance=kilometers(activity.distance),
                                   total_elevation_gain=activity.total_elevation_gain))

    title = 'Please choose your activity'
    option, index = pick(options=activities, title=title, options_map_func=get_label)

    update_activity(client, option.id, new_time)

