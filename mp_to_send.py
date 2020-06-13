#!/usr/bin/python3 

import csv
import datetime
import json
import sys
from typing import List

def strip_quotes(s: str):
    return s.replace('"', '')

class Send:
    def __init__(self, name: str, grade: str, date: str, location: str, style: str, notes: str):
        self.name = strip_quotes(name)
        self.grade = strip_quotes(grade)
        self.date = datetime.date.fromisoformat(date)
        self.location = strip_quotes(location)
        self.style = strip_quotes(style)
        self.notes = strip_quotes(notes)

    def __eq__(self, other):
        # test support
        if isinstance(other, self.__class__):
            return self.name == other.name and self.grade == other.grade and self.date == other.date and self.location == other.location and self.style == other.style and self.notes == other.notes
        return False

class SendEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Send):
            m = dict()
            m['__Send__'] = True
            m['name'] = obj.name
            m['grade'] = obj.grade
            m['date'] = str(obj.date)
            m['location'] = obj.location
            m['style'] = obj.style
            m['notes'] = obj.notes
            return m
        return json.JSONEncoder.default(self, obj)

def as_send(dct):
    if '__Send__' in dct:
        return Send(dct['name'], dct['grade'], dct['date'], dct['location'], dct['style'], dct['notes'])
    return dct

def convert_mp_csv(filename) -> List[Send]:
    with open(filename) as f:
        sends = list()
        reader = csv.reader(f, quotechar = '"', delimiter = ',')
        for row in reader:
             if row[11] == 'Boulder':
                 date = row[0]
                 name = row[1]
                 grade = row[2]
                 notes = row[3]
                 location = row[6]
                 style = row[9]
                 send = Send(name, grade, date, location, style, notes)
                 sends.append(send)
    return sends

def save(sends: List[Send], append: bool = False):
    if append:
        access_flag = 'a'
    else:
        access_flag = 'w'
    with open('ticks.json', access_flag) as f:
        f.write(json.dumps(sends, cls=SendEncoder, indent=4))


if __name__ == "__main__":
    filename = sys.argv[1]
    sends = convert_mp_csv(filename)
    save(sends)
    # s = json.dumps(sends, cls = SendEncoder)
    # f = json.loads(s, object_hook=as_send)

