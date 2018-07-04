# gpx-update

gpx-update - cli for updating gpx date

### Motivation
Import old activities from Strava to Relive

## Installation

### Requirements
* Python 3.5 and up

### Setup
Before the application can access the Strava API, it will need a Strava API token.
 
[Get a Strava API access token with write permission](https://yizeng.me/2017/01/11/get-a-strava-api-access-token-with-write-permission/)

Also API token can be generated using a separate program such as
[strava-tokengen](https://github.com/pR0Ps/strava-tokengen).



`gpx-update` expects to find a config file at `~/.config/strava-relive.ini` by default.

A sample has been included in this package. Copy the sample to the correct spot and set the API
token and other options.

### Installation from source
```
$ git clone https://github.com/andriyor/gpx-update-cli.git
$ cd gpx_update
$ python3 setup.py install
```

## Usage

### `--help`

```
$ gpx-update --help
Options:
  --new-time TEXT  specify date and time for all point current date by default
  --help           Show this message and exit.

Commands:
  file    Create updated GPX file
  id      Getting GPX file by activity id and upload to...
  pick    Getting GPX file by picked activity and...
  sfile   Updating GPX file from and upload to Strava
  strava  Login to Strava account
```

```
$ gpx-update file --help
Usage: gpx-update file [OPTIONS] INPUT_FILE_PATH

  Create updated GPX file

Options:
  --new   output file name with e.x old_name_new by default
  --ow    overwrite a file
  --ui    specify output file name manually
  --help  Show this message and exit.
```

```
$ gpx-update strava sfile --help
Usage: gpx-update sfile [OPTIONS] INPUT_FILE_PATH

  Updating GPX file from and upload to Strava
```

```
$ gpx-update strava id --help
Usage: gpx-update id [OPTIONS] ID

  Getting GPX file by activity id and upload to Strava
```

```
$ gpx-update strava pick --help
Usage: gpx-update pick [OPTIONS]

  Getting GPX file by picked activity and upload to Strava

Options:
  --before TEXT    Result will start with activities whose start date is
                   before specified date. (UTC)
  --after TEXT     Result will start with activities whose start date is after
                   specified value. (UTC)
  --limit INTEGER  How many maximum activities to return.
  --help           Show this message and exit.

```

### Example usage

```
$ head -15 1149478466.gpx
<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="StravaGPX" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">
 <metadata>
  <time>2017-08-08T07:39:12Z</time>
 </metadata>
 <trk>
  <name>Morning Ride</name>
  <type>1</type>
  <trkseg>
   <trkpt lat="49.5246470" lon="31.8017940">
    <ele>86.3</ele>
    <time>2017-08-08T07:39:12Z</time>
   </trkpt>
   <trkpt lat="49.5246280" lon="31.8020130">
    <ele>85.6</ele>

```

```
$ gpx-update 1149478466.gpx
```

```
$ head -15 1149478466_new.gpx         
<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="StravaGPX">
  <metadata>
    <time>2018-06-26T13:12:49Z</time>
  </metadata>
  <trk>
    <name>Morning Ride</name>
    <type>1</type>
    <trkseg>
      <trkpt lat="49.524647" lon="31.801794">
        <ele>86.3</ele>
        <time>2018-06-26T13:12:49Z</time>
      </trkpt>
      <trkpt lat="49.524628" lon="31.802013">
        <ele>85.6</ele>
```

```
gpx-update strava id 1492300979      
gpx-update strava file 1149478466.gpx
```

```
pipenv run gpx-update strava pick --limit=3 --before=2018-07-04

 Please choose your activity

 * 2018-06-28 16:37:33, Afternoon Ride, 2:31:17, 32.72 km, 327.90 m
   2018-06-22 18:56:08, Evening Ride, 0:40:06, 12.41 km, 113.80 m
   2018-06-15 18:50:08, Evening Ride, 1:13:38, 22.31 km, 186.20 m
```

## Development
Install [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```
