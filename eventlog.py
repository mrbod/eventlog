#!/usr/bin/env python
import sys
import struct
import collections

events = {
    0x00: 'EV_SYN', 0x01: 'EV_KEY', 0x02: 'EV_REL', 0x03: 'EV_ABS', 0x04: 'EV_MSC',
    0x05: 'EV_SW', 0x11: 'EV_LED', 0x12: 'EV_SND', 0x14: 'EV_REP', 0x15: 'EV_FF',
    0x16: 'EV_PWR', 0x17: 'EV_FF_STATUS', 0x1f: 'EV_MAX'
}

is64bit = sys.maxsize > 0xFFFFFFFF

# 30247657 691B0B00 0000 0000 01000000
if is64bit:
    event_struct = struct.Struct('QQHHi')
else:
    event_struct = struct.Struct('IIHHi')

class Event(collections.namedtuple('Event', 'sec event code value')):
    __slots__ = ()
    def __str__(self):
        return '{0.sec:.6f}: {0.event} {0.code} {0.value}'.format(self)

class EventHandler(object):
    def __init__(self, f):
        self.f = f
    def __iter__(self):
        return self
    def next(self):
        d = event_struct.unpack(self.f.read(event_struct.size))
        T = d[0] + d[1] / 1.0e6
        E = events.get(d[2], '?')
        return Event(T, E, *d[-2:])

try:
    eh = EventHandler(open(sys.argv[1], 'rb'))
    map(sys.stdout.write, (str(e) + '\n' for e in eh))
except KeyboardInterrupt:
    pass

