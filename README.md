# Hosting Interactive Python Notebooks on GitHub Pages

This repository demonstrates how to create an interactive Python notebook that
runs entirely in the browser, hosted for free on GitHub Pages. The notebook uses
marimo (a modern Python notebook engine), uv (for managing Python dependencies),
and WebAssembly (which lets Python run in your browser without a server).

## What This Setup Does

When you push code to this repository, GitHub automatically builds your notebook
into a static website and publishes it. Anyone can then visit the URL and
interact with your Python code directly in their browser—no installation
required on their end.

This happens through a GitHub Actions workflow (the automation that runs when
you push code). The workflow lives in `.github/workflows/deploy.yml` and handles
four main tasks: installing uv, setting up your Python environment, converting
your marimo notebook into a web-friendly format, and deploying it to GitHub
Pages.

## Getting Started

### Step 1: Enable GitHub Pages

First, you need to tell GitHub that you want to use Pages for this repository.
Go to your repository's Settings, then find the "Pages" section in the left
sidebar. Under "Source," select "GitHub Actions" instead of the default branch
option. This tells GitHub to use your workflow file to build and deploy the
site.

### Step 2: Create Your Notebook

Your Python notebook should be a `.py` file that uses marimo's format. The
example in this repo is `labkey_to_github.py`, which demonstrates how to work
with data and create interactive elements.

To edit your notebook locally, you'll need uv installed. The easiest way to
install it is:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once uv is installed, you can run `uv sync` in your repository folder to set up
the Python environment with all the dependencies listed in `pyproject.toml`.
Then start the marimo editor with:

```bash
uv run marimo edit labkey_to_github.py
```

This opens a local server where you can edit your notebook interactively.

### Step 3: Working with Data

If your notebook needs data files (like the `penguins.csv` example here), put
them in the `public/` folder. In your marimo notebook, you can reference these
files using `mo.notebook_location()` to get the path relative to your notebook
file:

```python
csv_path = mo.notebook_location() / "public" / "penguins.csv"
data = pl.read_csv(str(csv_path))
```

The `public/` folder gets included when the notebook is exported to WebAssembly,
making your data available in the browser.

### Step 4: Understanding the Deployment

When you push to the `main` branch, the GitHub Actions workflow automatically
kicks off. Here's what happens under the hood:

The workflow first installs uv using GitHub's pre-made action
(`astral-sh/setup-uv@v6`). Then it runs `uv sync`, which reads your
`pyproject.toml` file and installs all your Python dependencies into a virtual
environment—things like marimo, polars, and fastexcel in this example.

The key step is the export command:

```bash
uv run marimo export html-wasm labkey_to_github.py -o wasm_dir --mode run --show-code
```

This line does the heavy lifting. It converts your Python notebook into a
standalone HTML page that includes WebAssembly binaries (which let Python run in
the browser). The `--mode run` flag means the notebook will execute when someone
loads the page, and `--show-code` ensures the Python code is visible alongside
the output. The result goes into a folder called `wasm_dir`.

After the export, the workflow uploads that `wasm_dir` folder as a "Pages
artifact"—essentially packaging it up for deployment. A second job then takes
that artifact and publishes it to GitHub Pages using the `actions/deploy-pages`
action. This job has special permissions (`pages: write` and `id-token: write`)
that allow it to deploy to your Pages site.

### Step 5: Push and Deploy

Once everything is set up, just commit your changes and push to the `main`
branch:

```bash
git add .
git commit -m "Update notebook"
git push
```

GitHub will run the workflow automatically. You can watch its progress in the
"Actions" tab of your repository. When it's done (usually takes a minute or
two), your site will be live at
`https://[your-username].github.io/[repo-name]/`.

## Customizing Your Notebook

The notebook file itself is regular Python code with marimo's decorators. Each
`@app.cell` defines a cell in your notebook. You can add new cells, import
additional packages (just add them to `pyproject.toml`), and use any of marimo's
built-in UI elements like `mo.ui.dataframe()` or `mo.ui.data_explorer()`.

If you want to trigger a deployment manually (without pushing new code), you can
go to the Actions tab, select the "Deploy Marimo Notebook on GitHub" workflow,
and click "Run workflow." That's what the `workflow_dispatch` trigger in the
workflow file enables.

## Troubleshooting

If your workflow fails, check the Actions tab for error messages. Common issues
include forgetting to enable GitHub Pages in Settings, or having a dependency in
your notebook that isn't listed in `pyproject.toml`. The workflow logs are
usually pretty clear about what went wrong.

Remember that WebAssembly has some limitations—not every Python package works in
the browser. Marimo's documentation has a list of compatible packages, but
generally, pure Python packages and popular data libraries (like pandas, polars,
numpy) work well.

## What's Next

Once your notebook is deployed, anyone can visit the URL and interact with it.
They can run the code, explore the data, and see the results—all without
installing Python. This makes it perfect for sharing analyses, creating
interactive reports, or building educational materials.

The beauty of this setup is that it's all declarative—you just write Python,
push it, and GitHub handles the rest. No servers to manage, no hosting costs,
just automated deployment of your interactive notebooks.
