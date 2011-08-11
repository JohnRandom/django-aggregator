#-*- coding: utf-8 -*-
import time

class Struct(dict):
	'''
	An attempt to build a dict/object hybrid, that can be accessed in both ways.
	By inheriting from dict, we can assure that. On each part of the dict, the
	Struct is instantiated recursively.
	'''

	def __init__(self, dict_):
		super(Struct, self).__init__(dict_)
		for key in self:
			item = self[key]
			if isinstance(item, list):
				for idx, it in enumerate(item):
					if isinstance(it, dict):
						item[idx] = Struct(it)
			elif isinstance(item, dict):
				self[key] = Struct(item)

	def __getattr__(self, key):
		return self[key]

def entry():
	'''
	Some black magic is going on here in order to reproduce a nearly exact copy of a feedparser.entry object.

	First we have to monkeypatch time.struct_time to parse the values of the *_parsed fields, because they
	can't be pickled. The monkeypatch has to return a time.struct_time object itself, because we want the
	parsed object to behave exaclty like a feedparser.entry.

	Secondly, we need the dict to work as an object as well, because that's the way we want to handle it
	in the EntryWrapper, which is accessing the data of the structure like a dict as well as like an object.

	So far, this implementation seems to reproduce each testing case in such a way, that all tests pass.
	We just have to make sure, that we restore the time module monkeypatch back to it's original before
	we mess up things somewhere else.
	'''

	func = time.struct_time
	def _struct_time(tm_year=None, tm_mon=None, tm_mday=None, tm_hour=None, tm_min=None, tm_sec=None, tm_wday=None, tm_yday=None, tm_isdst=None):
		return time.localtime(time.mktime((tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)))
	time.struct_time = _struct_time

	struct = Struct({'author': u'macro',
		'author_detail': {'name': u'macro'},
		'authors': [{}],
		'comments': u'http://logbuch.c-base.org/archives/1170#comments',
		'content': [{'base': u'',
					 'language': None,
					 'type': 'text/html',
					 'value': u'<p><a href="http://logbuch.c-base.org/wp-content/uploads/2011/04/ubuntu_natty_narwhal.png"><img alt="" class="alignnone size-full wp-image-1171" src="http://logbuch.c-base.org/wp-content/uploads/2011/04/ubuntu_natty_narwhal.png" title="ubuntu_natty_narwhal" width="550" /></a><br />\n<br />\nZur Feier der Ver\xf6ffentlichung von Ubuntu 11.04 \u201eNatty Narwhal\u201c veranstaltet die Anwendergruppe \u201eUbuntu-Berlin\u201c nun schon zum elften Mal eine Releaseparty. Natty bringt neben anderen Verbesserungen auch bisher un\xfcbertroffene Unterst\xfctzung f\xfcr Multitouchger\xe4te mit, die einen Schwerpunkt des Vortragsprogramms bilden.</p>\n<p>* Datum: Samstag, der 21.05.2011<br />\n* Einlass: ab 15 Uhr, der Eintritt ist frei<br />\n* Vortr\xe4ge ab 16 Uhr<br />\n* Getr\xe4nke: erh\xe4ltlich an der Bar zu moderaten Preisen<br />\n* WLAN: vorhanden (kostenlos)</p>\n<p>Ort: c-base, Rungestra\xdfe 20<br />\nLageplan bei <a href="http://www.openstreetmap.de/karte.html?zoom=17&#038;lat=52.51298&#038;lon=13.42012&#038;layers=B0">http://www.openstreetmap.de</a></p>\n<p>Es gibt wie immer interessante Vortr\xe4ge f\xfcr Ein- und Umsteiger sowie f\xfcr erfahrene Ubuntu-Nutzer und Leute mit generellem Interesse an freier Software. Zwischen den drei\xdfigmin\xfctigen Vortr\xe4gen ist jeweils ca. eine Viertelstunde Pause.</p>\n<p>16:00 Neues bei Natty, inkl. Unity<br />\n16:45 Kubuntu<br />\n17:30 Wo finde ich Hilfe?<br />\n18:15 Virtual Box<br />\n19:00 Firefox und Thunderbird plattform\xfcbergreifend nutzen<br />\n19:45 Multitouch mit Natty<br />\n21:00 offene Talkrunde im Seminarraum</p>\n<p>Au\xdferdem werden CDs mit der neu erschienenen Version gegen eine kleine Spende abgegeben. Zudem k\xf6nnen mitgebrachte USB-Sticks mit der neuen Ubuntu-Version bespielt werden.</p>\n<p>Ansonsten ist ein fr\xf6hliches Miteinander in entspannter Lounge-Atmosph\xe4re angesagt. Lernt andere Benutzer des freien Betriebssystems Ubuntu kennen oder trefft ebenso Neugierige wie Euch.</p>\n<p><a href="http://ubuntu-berlin.de/natty-release-party">http://ubuntu-berlin.de/natty-release-party</a></p>\n<p>Ubuntu und seine Logos sind eingetragene Warenzeichen von Canonical Ltd. Der Flyer und der obige Text stehen unter der Lizenz Creative Commons CC-BY-SA 3.0.</p>'}],
		'guidislink': False,
		'id': u'http://logbuch.c-base.org/?p=1170',
		'link': u'http://logbuch.c-base.org/archives/1170',
		'links': [{'href': u'http://logbuch.c-base.org/archives/1170',
				   'rel': 'alternate',
				   'type': 'text/html'}],
		'slash_comments': u'0',
		'summary': u'Zur Feier der Ver\xf6ffentlichung von Ubuntu 11.04 \u201eNatty Narwhal\u201c veranstaltet die Anwendergruppe \u201eUbuntu-Berlin\u201c nun schon zum elften Mal eine Releaseparty. Natty bringt neben anderen Verbesserungen auch bisher un\xfcbertroffene Unterst\xfctzung f\xfcr Multitouchger\xe4te mit, die einen Schwerpunkt des Vortragsprogramms bilden. * Datum: Samstag, der 21.05.2011 * Einlass: ab 15 Uhr, der Eintritt ist frei * Vortr\xe4ge ab [...]',
		'summary_detail': {'base': u'',
						   'language': None,
						   'type': 'text/html',
						   'value': u'Zur Feier der Ver\xf6ffentlichung von Ubuntu 11.04 \u201eNatty Narwhal\u201c veranstaltet die Anwendergruppe \u201eUbuntu-Berlin\u201c nun schon zum elften Mal eine Releaseparty. Natty bringt neben anderen Verbesserungen auch bisher un\xfcbertroffene Unterst\xfctzung f\xfcr Multitouchger\xe4te mit, die einen Schwerpunkt des Vortragsprogramms bilden. * Datum: Samstag, der 21.05.2011 * Einlass: ab 15 Uhr, der Eintritt ist frei * Vortr\xe4ge ab [...]'},
		'tags': [{'label': None, 'scheme': None, 'term': u'bordleben'},
				 {'label': None, 'scheme': None, 'term': u'cience'},
				 {'label': None, 'scheme': None, 'term': u'com'}],
		'title': u'Ubuntu 11.04 \u201eNatty Narwhal\u201c Releaseparty 21.05.2011',
		'title_detail': {'base': u'',
						 'language': None,
						 'type': 'text/plain',
						 'value': u'Ubuntu 11.04 \u201eNatty Narwhal\u201c Releaseparty 21.05.2011'},
		'updated': u'Fri, 29 Apr 2011 19:11:43 +0000',
		'updated_parsed': time.struct_time(tm_year=2011, tm_mon=4, tm_mday=29, tm_hour=19, tm_min=11, tm_sec=43, tm_wday=4, tm_yday=119, tm_isdst=0),
		'wfw_commentrss': u'http://logbuch.c-base.org/archives/1170/feed'})

	time.struct_time = func
	return struct
