import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # This is a cool title

    Yay
    """)
    return


@app.cell
def _(pl):
    penguins_pl = pl.read_csv("penguins.csv")
    return (penguins_pl,)


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
