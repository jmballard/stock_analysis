import os
import sys

import pandas as pd

# Add the parent directory of this file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from reporting.report import Report  # noqa


def test_init():
    nb = Report("Title")

    # nb.add_section("TEst","test")

    assert nb["nbformat"] == 4
    assert nb["nbformat_minor"] == 5
    assert nb["metadata"] == {}
    print(nb["cells"])

    for cell in nb["cells"]:
        keys_no_id = [key for key in cell.keys() if key != "id"]
        for key in keys_no_id:
            assert cell[key]
    assert nb["cells"] == [
        {
            "id": "a698c58b",
            "cell_type": "markdown",
            "source": "# Title",
            "metadata": {},
        },
        {
            "id": "aa0152ea",
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "source": '\nfrom IPython.core.display import HTML\nHTML(open("report_style.css").read())\n        ',
            "outputs": [],
        },
    ]

    ## THE ID CHANGE


test_init()
