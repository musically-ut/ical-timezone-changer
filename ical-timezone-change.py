#!/usr/bin/env python
from __future__ import print_function
import iso8601 as iso
import datetime as D
import re
import sys
import click

dttartRegEx = re.compile('^(DTSTART(;.*)?:)(.*)$')
dtendRegEx = re.compile('^(DTEND(;.*)?:)(.*)$')

def fmt_ical_time(time):
    '''Returns the time in UTC timezone with 'Z' suffix.'''
    return time.astimezone(iso.UTC).strftime('%Y%m%dT%H%M%SZ')

def time_line_xform(regMatch, delta, idx):
    '''Transforms a reg-ex match object of a time line by delta.'''
    if regMatch is None:
        print('Ill formatted line: ', idx)
        sys.exit(-1)
    else:
        prefix = regMatch.group(1)
        time = iso.parse_date(regMatch.group(3))
        return prefix + fmt_ical_time(time + delta)

@click.command()
@click.argument('input_calendar', type=click.File('r'))
@click.option('--hours',
              type=float,
              prompt='How many hours to offset by (can be -ve)',
              help='Number of hours to shift time by')
@click.option('--output', 'output_calendar',
              type=click.File('w'),
              default=sys.stdout,
              help='File to write the output to.')
def run(input_calendar, hours, output_calendar):
    delta = D.timedelta(hours=hours)
    for idx, line in enumerate(input_calendar):
        if line.startswith('DTSTART'):
            regMatch = dttartRegEx.match(line.strip())
            output_calendar.write(time_line_xform(regMatch, delta, idx) + '\n')
        elif line.startswith('DTEND'):
            regMatch = dtendRegEx.match(line.strip())
            output_calendar.write(time_line_xform(regMatch, delta, idx) + '\n')
        else:
            output_calendar.write(line)

if __name__ == '__main__':
    run()
