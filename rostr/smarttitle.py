import re
from datetime import datetime, timedelta as delta



class InvalidTimeException():
	pass

def cl_shorttime(title, start, end, reference, matched_group):
	hour = str(int(reference.strftime('%I')))
	minute = int(reference.strftime('%M'))
	ampm = reference.strftime('%p')

	if minute == 0:
		time = "%s %s" % (hour, ampm)
	else:
		time = "%s:%s %s" % (hour, minute, ampm)

	return title.replace(matched_group[0], time)

def cl_duration(title, start, end, reference, matched_group):
	duration = end - start
	hours, minutes = divmod(duration.seconds / 60, 60)
	hours = float(hours)
	dur = hours + (minutes / 60.0)
	if dur % 1 == 0: dur = int(dur)
	return title.replace(matched_group[0], str(dur))

language = {
	'h': '%I',         # hour, 12 hour time
	'H': '%H',         # hour, 24 hour time
	'm': '%M',         # minute
	'p': '%p',         # am or pm
	'n': '%b',         # month abbreviated name, Nov
	'T': '%I:%M %p',   # time shortcut, 09:30 AM
	't': cl_shorttime, # time shortcut, short as possible (8 AM, 7:30 PM)
	'l': cl_duration   # Duration of shift
}

def format(title, start, end):
	find = re.compile(r'(\{(?:(\w+)\.)?(\w)\})')
	results = find.findall(title)
	formatted = title

	for groups in results:

		if groups[1]:
			if groups[1] == 'start':
				reference = start
			elif groups[1] == 'end':
				reference = end
			else:
				return title
				# raise InvalidTimeException
		else:
			reference = start

		if groups[2] in language:
			code = language[groups[2]]
		else:
			code = "%" + groups[2]

		# Some codes are 'custom' and will be a function instead of a strftime code
		if hasattr(code, '__call__'):
			formatted = code(formatted, start, end, reference, groups)
		else:
			formatted = formatted.replace(groups[0], code)
			formatted = reference.strftime(title)


	return formatted


if __name__ == '__main__':
	start = datetime.now() - delta(days=1, hours=10)
	start = start.replace(minute=10, hour=15)
	end = start + delta(hours=6)

	print
	print "Start:\t %s" % start.strftime("%a %d %b, %I:%M %p")
	print "End:\t %s" % end.strftime("%a %d %b, %I:%M %p" )
	print

	titles = [
		"Shift: {start.t}",
		"{start.a} - Work",
		"Shift{start.a}",
		"Shift: {a}",
		"Shift: {df.a}",
		"{a} - Work",
		"Shift{a}",
		"Work (end: {end.h} {end.p})",
		"Work (end: {end.t})",
		"Work (end: {end.T})",
	]

	for s in titles:
		print s
		try:
			print format(s, start, end)
		except InvalidTimeException:
			print 'Invalid time!'
		print
