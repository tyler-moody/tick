import json
import pytest
import tempfile

import tick


def test_encode_decode():
    send = tick.Send("name", "grade", "2000-01-01", "location", "style", "notes")
    encoded = json.dumps(send, cls=tick.SendEncoder)
    decoded = json.loads(encoded, object_hook=tick.as_send)
    assert send == decoded


def test_save_load():
    send = tick.Send("name", "grade", "2000-01-01", "location", "style", "notes")
    sends = list()
    sends.append(send)
    sends.append(send)
    with tempfile.NamedTemporaryFile() as f:
        filename = f.name
        tick.save(filename, sends)
        loaded = tick.load(filename)
    assert loaded == sends


def test_convert_mp_csv():
    with tempfile.NamedTemporaryFile() as f:
        filename = f.name
        mp_content = b"""2020-06-07,"The Hole",V6,,https://www.mountainproject.com/route/106807930/the-hole,1,"Washington > Central-East Cascades, Wenatchee, & Leavenworth > Icicle Creek > ** Bouldering in Icicle Creek > Mad Meadows",3.4,-1,Send,,Boulder,,10,20600"""
        f.write(mp_content)
        f.seek(0)
        mp_sends = tick.convert_mp_csv(f.name)

        send = tick.Send(
            "The Hole",
            "V6",
            "2020-06-07",
            "Washington > Central-East Cascades, Wenatchee, & Leavenworth > Icicle Creek > ** Bouldering in Icicle Creek > Mad Meadows",
            "Send",
            "",
        )
        assert send == mp_sends[0]


def test_filter_by_date_before():
    sends = list()
    sends.append(tick.Send("before", "v0", "1999-12-31", "location", "send", "notes",))
    sends.append(tick.Send("after", "v0", "2000-01-01", "location", "send", "notes",))
    filtered = tick.filter_by_date(sends, "2000-01-01", tick.DateComparison.BEFORE)
    assert len(filtered) == 1
    assert filtered[0].name == 'before'

def test_filter_by_date_after():
    sends = list()
    sends.append(tick.Send("before", "v0", "1999-12-31", "location", "send", "notes",))
    sends.append(tick.Send("after", "v0", "2000-01-01", "location", "send", "notes",))
    filtered = tick.filter_by_date(sends, "2000-01-01", tick.DateComparison.AFTER)
    assert len(filtered) == 1
    assert filtered[0].name == 'after'
