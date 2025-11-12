import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hosting Python Notebooks as Static Sites on GitHub Pages

    Sometimes, when performing exploratory analyses, we'd like to share a preliminary analysis with our collaborators without requiring that they set up an environment for programming Python themselves. In theory, the internet is an ideal system for this, but sharing executable code in a browser-reanderable format has traditionally only been possible with the languages of the web: HTML, CS, and JavaScript. Analyses in Python have thus existed behind a higher barrier of entry--to re-run, say, a Jupyter notebook, users must set up their own python environment, install jupyter, and install any dependencies themselves, all of which can be nontrivial for beginners and noncoders.

    Recently, this story has changed considerably for Python. A number of newer technologies are now mature that make it easier than ever to deploy and acsess python analyses through the internet.

    This notebook demonstrates one set of technologies that can be used to trivially share a Python analysis. In brief, this set includes:

    1. [uv](https://docs.astral.sh/uv/), a command line utility for rapidly generating reproducible python environments, including dependencies
    2. [marimo notebooks](https://marimo.io/), a modern python notebook engine that can execute Python in the browser via a technology called WebAssembly
    3. [GitHub Pages](https://docs.github.com/en/pages), a static site hosting solution that can be accessed via any GitHub repository.

    Users should refer to this repo's README.md file for instructions on setting up this demo. The remainder of this notebook will address only the Python notebook elements themselves.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Initial setup

    _NOTE:_ This notebook assumes that it's running within a Python virtual environment where `polars` and `marimo` itself is installed. The following imports of those tools will error if these dependencies are not installed
    """)
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In addition to imports, this notebook also has a _data dependency_: the `penguins.csv` file, stored in the `public/` directory of this repo.

    To access this data within the static site context, we need a little more handling than usual, as follows. This handling is [documented in greater detail in the Marimo docs]([https://docs.marimo.io/guides/wasm/#packages](https://docs.marimo.io/guides/wasm/#including-data)).
    """)
    return


@app.cell
def _(mo):
    csv_path = mo.notebook_location() / "public" / "penguins.csv"
    return (csv_path,)


@app.cell
def _(csv_path, pl):
    penguins_pl = pl.read_csv(str(csv_path))
    return (penguins_pl,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Interactive Element in Marimo

    One of the primary benefits of Marimo aside from its browser-compatible execution engine is that it comes with many UI elements that are helpful for data exploration built-in. To follow are two such elements: a dataframe viewer with no-code exploration tools, and the data explorer element, which allows you to create data visualizations on the fly, again without code.

    As you explore the Palmer Penguins dataset in both, I recommend you see if you can do all of the following items:

    #### The DataFrame Element
    1. Be able to sort the data by one of the columns and also clear the sort.
    2. Tell Marimo to show more than 5 rows by default.
    3. Add one or two data transformations to filter or otherwise manipulate the data frame.
    4. See what Python code your data transformations corresponds to.
    5. Download the dataset from the UI element as a JSON, CSV, or Parquet file, or by pasting into your clipboard.

    #### The Data Explorer Element
    1. Find two quantitative columns and make a scatter plot.
    2. Create a row-faceted visualization
    3. Create a column-faced visualization
    4. Make a line or a box plot.
    5. EXport your visualizations as a PNG or a SVG.
    """)
    return


@app.cell
def _(mo, penguins_pl):
    mo.ui.dataframe(penguins_pl)
    return


@app.cell
def _(mo, penguins_pl):
    mo.ui.data_explorer(penguins_pl)
    return


if __name__ == "__main__":
    app.run()
