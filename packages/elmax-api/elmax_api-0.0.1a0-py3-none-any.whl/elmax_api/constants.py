"""Constants for the Elmax Cloud service client."""

from . import __version__


# URL Constants
# TODO: uncomment the following
# BASE_URL = "https://cloud.elmaxsrl.it"
BASE_URL = "https://test.fabiozingaro.com"
ENDPOINT_DEVICES = "api/ext/devices"
# TODO: Seems not the corrent one
# ENDPOINT_LOGIN = "api/ext/login"
ENDPOINT_LOGIN = "api/ext/login"
ENDPOINT_STATUS_ENTITY_ID = "api/ext/status"
ENDPOINT_ENTITY_ID_COMMAND = "api/ext"
ENDPOINT_DISCOVERY = "api/ext/discovery"

# User agent
USER_AGENT = f"elmax-api/{__version__}"

# DEFAULT HTTP TIMEOUT
DEFAULT_HTTP_TIMEOUT = 10.0
BUSY_WAIT_INTERVAL = 2.0



