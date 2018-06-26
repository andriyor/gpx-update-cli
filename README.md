# gpx-update

gpx-update - cli for updating gpx date

### Motivation
Import old activities from Strava to Relive

## Installation

### Requirements
* Python 3.5 and up

### Installation from source
```
$ git clone https://github.com/andriyor/flibusta-dl.git
$ cd gpx_update
$ python3 setup.py install
```

## Usage

### `--help`

```
$ gpx-update --help
Usage: gpx-update [OPTIONS] INPUT_FILE_PATH

Options:
  --new-time TEXT  specify date and time for all point current date by default
  --new            output file name with e.x old_name_new by default
  --ow             overwrite a file
  --ui             specify output file name manually
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

## Development
Install [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```

### TODO
- [ ] strava integration
