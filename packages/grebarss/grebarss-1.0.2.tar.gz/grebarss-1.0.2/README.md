# rss_reader 

A command-line utility for reading news with RSS, written in Python 3.9. The utility written as a final task for EPAM Python Training 2021.09  

## Installation

$ pip install rss_reader

## Usage

- Find and copy URL for RSS source
- rss_reader [URL]
- Help: rss_reader -h

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Pure Python command-line RSS reader.

positional arguments:
  source         URL RSS

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

### --json

In case of using --json argument utility convert the news into JSON format. JSON structure:
- The data are in name/value pairs
- Data objects are separated by commas.
- Curly braces {} hold objects
- Square brackets [] hold arrays.
- Each data element is enclosed with quotes "" if it is a character, or without quotes if it is a numeric value.

Example of item containing news:
{
  "item: [
    {"title": "title_data"},
    {"pubDate": "pubDate_data"},
    {"link": "link_data"}
  ]
}

## License

...

## Contact

Follow me on LinkedIn - https://www.linkedin.com/in/alexander-greben-87209319b/


