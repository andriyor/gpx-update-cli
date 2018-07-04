from setuptools import setup

setup(
    name='gpx-update',
    version='0.1',
    py_modules=['gpx-update'],
    install_requires=['gpxpy', 'click', 'python-dateutil', 'stravaweblib', 'halo', 'pick'],
    entry_points='''
        [console_scripts]
        gpx-update=gpx_update.gpx_update:cli
    ''',
)