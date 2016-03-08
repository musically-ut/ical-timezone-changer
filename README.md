# ical timezone changer

This script can be used to change all the start and end times on a calendar's events by a fixed offset.

It has been worked to test only with:

 - Google Calendar exports (which export the UTC time instead of floating local times).
 - Static events with known start/end date-times (no recurring events).

Example run:

    ./ical-timezone-change.py ~/tmp/input.ics --hours=-9 --output ~/tmp/output.ics

