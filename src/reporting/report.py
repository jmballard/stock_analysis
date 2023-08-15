import os
import subprocess

import nbformat
import papermill as pm


class Report:
    def __init__(self, title):
        nb = nbformat.v4.new_notebook()

        nb["cells"].append(nbformat.v4.new_markdown_cell("# " + title))

        nb["cells"].append(
            nbformat.v4.new_code_cell(
                """
from IPython.core.display import HTML
HTML(open("report_style.css").read())
        """
            )
        )

        self.notebook = nb

    def __str__(self):
        return str(self.notebook)

    def __getitem__(self, item):
        return getattr(self.notebook, item)

    def add_markdown_cell(self, text):
        """Add markdown cell.

        Add a markdown cell to notebook.

        Args:
            text (str): text to add in the cell
        """
        self.notebook["cells"].append(nbformat.v4.new_markdown_cell(text))

    def add_toc(self, sections):
        """Add table of contents.

        Add a table of contents with link. Need a dictionary as input that contains the titles of the sections with their link.

        Args:
            sections (dict): sections with their links
        """
        TOC = "## Table of Contents\n"
        for section_name, link in sections.items():
            TOC += "[{}](#{})<br>\n".format(section_name, link)

        self.notebook["cells"].append(nbformat.v4.new_markdown_cell(TOC))

    def add_section(self, section_name, link):
        """Add section (with link).

        _extended_summary_

        Args:
            section_name (_type_): _description_
            link (_type_): _description_
        """
        self.notebook["cells"].append(
            nbformat.v4.new_markdown_cell(f'## {section_name} <a id="{link}"></a>')
        )

    def add_code_cell(self, text):
        """Add code cell.

        Add a code cell to notebook.

        Args:
            text (str): code to add in the cell (between quote marks)
        """
        self.notebook["cells"].append(nbformat.v4.new_code_cell(text))

    def get_cells(self):
        """Get cells.

        Get list of cells from notebook

        Returns:
            list: cells of the notebook.
        """
        return self.notebook["cells"]

    def execute(self, path_to_file, convert_to_html=True):
        """Execute the notebook.

        In this function, we will create the jupyter notebook we manually created, then execute it and - if we want - convert it to html.

        Args:
            path_to_file (str): file path where we want our file to be save (.ipynb extension)
            convert_to_html (bool, optional): Flag if we want the notebook in html format. Defaults to True.
        """
        self.notebook["metadata"] = {
            "kernelspec": {
                "display_name": "python3",
                "language": "python",
                "name": "python3",
            }
        }
        nbformat.write(self.notebook, "outputs/output_notebook.ipynb")

        # run the report
        pm.execute_notebook(
            "outputs/output_notebook.ipynb", path_to_file, parameters=dict()
        )
        os.remove("outputs/output_notebook.ipynb")

        # if we want to convert, we will keep only the html version
        if convert_to_html:
            # create the html version
            subprocess.run(
                r'jupyter nbconvert --to html "output_run_notebook.ipynb" --no-input',
                check=True,
                shell=True,
            )

            # delete the ipynb files
            os.remove(path_to_file)
