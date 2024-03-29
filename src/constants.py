from pathlib import Path

MAIN_DOC_URL = "https://docs.python.org/3/"
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
BASE_DIR = Path(__file__).parent
PEP_URL = "https://peps.python.org/"
EXPECTED_STATUS = {
    "A": ("Active", "Accepted"),
    "D": ("Deferred",),
    "F": ("Final",),
    "P": ("Provisional",),
    "R": ("Rejected",),
    "S": ("Superseded",),
    "W": ("Withdrawn",),
    "": ("Draft", "Active"),
}
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = "%d.%m.%Y %H:%M:%S"
