from datetime import datetime as dt, timedelta
from decimal import Decimal
import random
import string
import json
import re

from django.http import HttpResponse
from django.utils.timezone import now as dtnow

from dateutil import parser

from models import Roster, Store


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def un2x(store):
    store.image = store.image.replace('_2x', '')
    return store


def limit(msg, limit):
    if len(msg) > limit:
        return msg[:limit]
    else:
        return msg


def unique(arg):
    output = []
    prev = ''
    for t in arg:
        if t != prev:
            output.append(t)
        prev = t

    return output


def JSONError(msg, status=400):
    json_response = {
        "status": "error",
        "message": msg
    }
    return HttpResponse(json.dumps(json_response), status=status)


def ParseError(msg, request, status=400):
    caltitle    = request.POST.get("title", '')
    callocation = request.POST.get("location", '')
    shiftinput  = request.POST.get("roster", None)

    if not caltitle:
        caltitle = request.GET.get("title", '')
    if not callocation:
        callocation = request.GET.get("location", '')

    dbroster = Roster(
        event_title=caltitle,
        event_location=callocation,
        raw_roster=shiftinput,
        method='site',
        created=dtnow(),
        success=False,
        error=msg
    )

    if request.POST.get('bm', False):
        dbroster.method = 'bookmarklet'
        dbroster.version = request.POST.get('v', '_none_')

    dbroster.save()

    return JSONError(msg, status)


def makeAccessCode(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(length))


def find_store(roster):
    foundstore = None
    display_location = None
    structured_location = None

    rollout = re.compile(r'\b((?:R|r)\d{3})\b')
    namefilter = re.compile(r'(Apple|Store|Retail|,|-|_|:)')
    junkchars = ' -_:,'

    if rollout.match(roster.event_location):
        matchedrollout = roster.event_location.upper()
        matchedstore = Store.objects.filter(number=matchedrollout)

        if matchedstore:
            foundstore = matchedstore[0]
    else:
        choices = []
        location = roster.event_location
        choices.append(location)

        location = location.strip(' -_:,')
        choices.append(location)

        location = namefilter.sub('', roster.event_location).strip(' -_:,')
        choices.append(location)

        matchedstore = Store.objects.filter(name__in=choices)
        if matchedstore:
            foundstore = matchedstore[0]

    if not foundstore:
        choices = []
        title = roster.event_title
        choices.append(title)

        title = title.strip(junkchars)
        choices.append(title)

        title = namefilter.sub('', roster.event_title).strip(junkchars)
        choices.append(title)

        matchedstore = Store.objects.filter(name__in=choices)
        if matchedstore:
            foundstore = matchedstore[0]

    if foundstore:
        # roster.store = foundstore
        display_location = "Apple Store, %s\n%s" % (foundstore.name, foundstore.address)
        display_location = "\\n".join(display_location.splitlines())
        x_title = "\"Apple Store, %s\"" % foundstore.name
        x_address = foundstore.address.replace('\\n', '\\\\n')

        lat = str(Decimal(foundstore.geoposition.latitude).quantize(Decimal('1.000000')))
        llong = str(Decimal(foundstore.geoposition.longitude).quantize(Decimal('1.000000')))
        structured_location = "VALUE=URI;"
        structured_location += "X-ADDRESS=%s;" % x_address
        structured_location += "X-APPLE-RADIUS=72;"
        structured_location += "X-TITLE=%s:" % x_title
        structured_location += "geo:%s,%s" % (lat, llong)

    return foundstore, display_location, structured_location


def parse_roster(raw_roster, sat=False):
    EMPTYSHIFT = '00:00AM'
    roster = []
    hours_accumulative = timedelta(hours=0)

    shifts_regex_str = r'^(?P<day>(?:Satur|Sun|Mon|Tues|Wednes|Thurs|Fri)day)?[a-zA-Z\s]*(?P<start>\d{1,2}:\d{2}[PAM]{2})[a-zA-Z\s]*(?P<end>\d{1,2}:\d{2}[PAM]{2})'
    sat_regex_str = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1,5}(\d{2}),?\s{1,5}(2\d{3})'

    shifts_regex = re.compile(shifts_regex_str, flags=re.MULTILINE)
    sat_regex = re.compile(sat_regex_str)

    if not sat:
        matched_sat = sat_regex.findall(raw_roster)
        if len(matched_sat) != 1:
            return False

        sat_str = ' '.join(matched_sat[0])
        sat = dt.strptime(sat_str, "%b %d %Y")

    matched_shifts = shifts_regex.findall(raw_roster)

    # We can't always rely on Saturday being the first day of the
    # So, we make a deltas dict based on the sat variable.
    deltas = {}
    for i in range(7):
        thisday = sat + timedelta(days=i)
        x = {thisday.strftime("%A"): timedelta(days=i)}
        deltas.update(x)

    for row in matched_shifts:
        day_raw = row[0]
        start_raw = row[1]
        end_raw = row[2]

        if start_raw != EMPTYSHIFT and end_raw != EMPTYSHIFT:
            # They're working today.

            split_shift = False if day_raw else True

            if not split_shift:
                # A split shift always has to come after a regular shift
                delta = deltas[day_raw]

            start = (sat + delta).strftime("%m-%d-%Y ") + start_raw
            end   = (sat + delta).strftime("%m-%d-%Y ") + end_raw
            start = parser.parse(start)
            end   = parser.parse(end)

            if end < start:
                # account for overnighters
                end = end + timedelta(days=1)

            if start != end:
                hours_accumulative += end - start
                roster.append({
                    'date': sat + delta,
                    'start': start,
                    'end': end,
                    'hours': end - start,
                })

    return sat, roster, hours_accumulative


class terminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

    def green(self, msg):
        return "%s%s%s" % (self.OKGREEN, msg, self.ENDC)
