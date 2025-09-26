# {{cookiecutter.project_name}}
{{cookiecutter.description}}

# Project Organization


```
    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make install`,  `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── artifacts          <- Deployable files to be synced to __s3__, this typically some json and ini files
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── environment.yml    <- conda environment setup with development-time packages to install
    │
    ├── pyproject.toml     <- python module configuration and dependencies
    │
    ├── src                <- Source code for use in this project.
    │   └── {{cookiecutter.module_name}}    <- Python module
    │       ├── __init__.py    <- Makes the Python module
    │       │
    │       ├── config .py     <- Configuration script loaded automatically           
    │       │
    │       ├── dataset.py     <- Scripts to download or generate data           
    │       │
    │       ├── features.py       <- Scripts to turn raw data into features for modeling
    │       │
    │       ├── modeling         <- Scripts to train models and then use trained models to make
    │       │   │                 predictions
    │       │   ├── predict.py
    │       │   └── train.py
    │       │
    │       └── plots.py       <- Scripts to create exploratory and results oriented visualizations
    │
    └── test                   <- tests source code
```

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/stellarshenson/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
