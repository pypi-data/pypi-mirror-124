import re

START_VERSION = '1.0.0'
VERSION_DELIMITER = '.'

RE_VERSION = re.compile(r'^[\d]+.[\d]+.[\d]+$')

# messages
THERE_IS_NO_VERSION_DATA = 'There is no data for this version'
DOES_NOT_EXIST_VERSION = 'Version {0} does not exist'
