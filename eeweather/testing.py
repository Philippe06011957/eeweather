from io import BytesIO
import pkg_resources
import re
import tempfile

from eeweather.cache import KeyValueStore


def write_isd_file(bytes_string):
    with pkg_resources.resource_stream('eeweather.resources', 'ISD.gz') as f:
        bytes_string.write(f.read())

def write_tmy3_file():
    data = pkg_resources.resource_string('eeweather.resources', '722880TYA.CSV')
    return data.decode('ascii')

def write_cz2010_file():
    data = pkg_resources.resource_string('eeweather.resources', '722880_CZ2010.CSV')
    return data.decode('ascii')

def write_missing_isd_file(bytes_string):
    with pkg_resources.resource_stream('eeweather.resources', 'ISD-MISSING.gz') as f:
        bytes_string.write(f.read())


def write_gsod_file(bytes_string):
    with pkg_resources.resource_stream('eeweather.resources', 'GSOD.op.gz') as f:
        bytes_string.write(f.read())


def write_missing_gsod_file(bytes_string):
    with pkg_resources.resource_stream('eeweather.resources', 'GSOD-MISSING.op.gz') as f:
        bytes_string.write(f.read())


class MockTMY3RequestProxy():

    def get_text(self, url):

        match_url = (
            "http://rredc.nrel.gov/solar/old_data/nsrdb/"
            "1991-2005/data/tmy3/722880TYA.CSV"
            )
        if re.match(match_url, url):
            return write_tmy3_file()



class MockCZ2010RequestProxy():

    def get_text(self, url):

        match_url = (
            "https://storage.googleapis.com/oee-cz2010/csv/"
            "722880_CZ2010.CSV"
            )

        if re.match(match_url, url):
            return write_cz2010_file()


class MockNOAAFTPConnectionProxy():

    def read_file_as_bytes(self, filename):
        bytes_string = BytesIO()

        if re.match('/pub/data/noaa/2007/722874-93134-2007.gz', filename):
            write_isd_file(bytes_string)
        elif re.match('/pub/data/noaa/2006/722874-93134-2006.gz', filename):
            write_missing_isd_file(bytes_string)
        elif re.match('/pub/data/gsod/2007/722874-93134-2007.op.gz', filename):
            write_gsod_file(bytes_string)
        elif re.match('/pub/data/gsod/2006/722874-93134-2006.op.gz', filename):
            write_missing_gsod_file(bytes_string)

        bytes_string.seek(0)
        return bytes_string


class MockKeyValueStoreProxy():

    def __init__(self):
        # create a new test store in a temporary folder
        self.store = KeyValueStore('sqlite:///{}/cache.db'.format(tempfile.mkdtemp()))

    def get_store(self):
        return self.store
