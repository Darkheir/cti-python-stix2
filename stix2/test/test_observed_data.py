import datetime as dt
import re

import pytest
import pytz
import stix2

from .constants import OBSERVED_DATA_ID

EXPECTED = """{
    "created": "2016-04-06T19:58:16Z",
    "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "first_observed": "2015-12-21T19:00:00Z",
    "id": "observed-data--b67d30ff-02ac-498a-92f9-32f845f448cf",
    "last_observed": "2015-12-21T19:00:00Z",
    "modified": "2016-04-06T19:58:16Z",
    "number_observed": 50,
    "objects": {
        "0": {
            "type": "file"
        }
    },
    "type": "observed-data"
}"""


def test_observed_data_example():
    observed_data = stix2.ObservedData(
        id="observed-data--b67d30ff-02ac-498a-92f9-32f845f448cf",
        created_by_ref="identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
        created="2016-04-06T19:58:16Z",
        modified="2016-04-06T19:58:16Z",
        first_observed="2015-12-21T19:00:00Z",
        last_observed="2015-12-21T19:00:00Z",
        number_observed=50,
        objects={
            "0": {
              "type": "file",
            },
        },
    )

    assert str(observed_data) == EXPECTED


@pytest.mark.parametrize("data", [
    EXPECTED,
    {
        "type": "observed-data",
        "id": "observed-data--b67d30ff-02ac-498a-92f9-32f845f448cf",
        "created": "2016-04-06T19:58:16Z",
        "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
        "first_observed": "2015-12-21T19:00:00Z",
        "last_observed": "2015-12-21T19:00:00Z",
        "modified": "2016-04-06T19:58:16Z",
        "number_observed": 50,
        "objects": {
            "0": {
                "type": "file"
            }
        }
    },
])
def test_parse_observed_data(data):
    odata = stix2.parse(data)

    assert odata.type == 'observed-data'
    assert odata.id == OBSERVED_DATA_ID
    assert odata.created == dt.datetime(2016, 4, 6, 19, 58, 16, tzinfo=pytz.utc)
    assert odata.modified == dt.datetime(2016, 4, 6, 19, 58, 16, tzinfo=pytz.utc)
    assert odata.first_observed == dt.datetime(2015, 12, 21, 19, 0, 0, tzinfo=pytz.utc)
    assert odata.last_observed == dt.datetime(2015, 12, 21, 19, 0, 0, tzinfo=pytz.utc)
    assert odata.created_by_ref == "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff"
    assert odata.objects["0"].type == "file"


@pytest.mark.parametrize("data", [
    """"0": {
        "type": "artifact",
        "mime_type": "image/jpeg",
        "payload_bin": "VBORw0KGgoAAAANSUhEUgAAADI=="
    }""",
    """"0": {
        "type": "artifact",
        "mime_type": "image/jpeg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/JPEG_example_JPG_RIP_100.jpg",
        "hashes": {
            "MD5": "6826f9a05da08134006557758bb3afbb"
        }
    }""",
])
def test_parse_artifact_valid(data):
    odata_str = re.compile('"objects".+\},', re.DOTALL).sub('"objects": { %s },' % data, EXPECTED)
    odata = stix2.parse(odata_str)
    assert odata.objects["0"].type == "artifact"


@pytest.mark.parametrize("data", [
    """"0": {
        "type": "artifact",
        "mime_type": "image/jpeg",
        "payload_bin": "abcVBORw0KGgoAAAANSUhEUgAAADI=="
    }""",
    """"0": {
        "type": "artifact",
        "mime_type": "image/jpeg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/JPEG_example_JPG_RIP_100.jpg",
        "hashes": {
            "MD5": "a"
        }
    }""",
])
def test_parse_artifact_invalid(data):
    odata_str = re.compile('"objects".+\},', re.DOTALL).sub('"objects": { %s },' % data, EXPECTED)
    with pytest.raises(ValueError):
        stix2.parse(odata_str)

# TODO: Add other examples
