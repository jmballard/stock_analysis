import os
import sys

import pandas as pd

# Add the parent directory of this file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from reporting.report import Report  # noqa


def test_init():
    nb = Report("Title")

    assert nb["nbformat"] == 4
    assert nb["nbformat_minor"] == 5
    assert nb["metadata"] == {}

    to_check = [
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

    # first, assess they have same number of cells
    assert len(nb["cells"]) == len(to_check)

    for cell_i in range(len(nb["cells"])):
        nb_cell = nb["cells"][cell_i]
        to_check_cell = to_check[cell_i]
        keys_no_id = [key for key in nb_cell.keys() if key != "id"]
        for key in keys_no_id:
            # check that the
            assert nb_cell[key] == to_check_cell[key]


def test_add_markdown_cell():
    text_to_add = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce aliquet est ipsum,
at tempus augue suscipit vitae. Pellentesque habitant morbi tristique senectus et
netus et malesuada fames ac turpis egestas. Sed id volutpat augue.

Duis porta molestie lacus ut feugiat. Aenean rutrum quis erat at sagittis.
Sed sollicitudin odio et risus laoreet interdum.
    """
    nb = Report("Title")
    nb.add_markdown_cell(text_to_add)

    assert nb["cells"][-1]["source"] == text_to_add
    assert nb["cells"][-1]["cell_type"] == "markdown"


def test_add_toc():
    TOC_result = """## Table of Contents
[section1](#sec1)<br>
[section2](#sec2)<br>
"""
    nb = Report("Title")
    nb.add_toc({"section1": "sec1", "section2": "sec2"})
    assert nb["cells"][-1]["source"] == TOC_result


def test_add_section():
    to_match = '## section1 <a id="sec1"></a>'
    nb = Report("Title")
    nb.add_section("section1", "sec1")
    assert nb["cells"][-1]["source"] == to_match


def test_add_code_cell():
    text_to_add = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce aliquet est ipsum,
at tempus augue suscipit vitae. Pellentesque habitant morbi tristique senectus et
netus et malesuada fames ac turpis egestas. Sed id volutpat augue.

Duis porta molestie lacus ut feugiat. Aenean rutrum quis erat at sagittis.
Sed sollicitudin odio et risus laoreet interdum.
    """
    nb = Report("Title")
    nb.add_code_cell(text_to_add)

    assert nb["cells"][-1]["source"] == text_to_add
    assert nb["cells"][-1]["cell_type"] == "code"


def test_get_cells():
    nb = Report("Title")
    assert nb.get_cells() == nb.notebook["cells"]
