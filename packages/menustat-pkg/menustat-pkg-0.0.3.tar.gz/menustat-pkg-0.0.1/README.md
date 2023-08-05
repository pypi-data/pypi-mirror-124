# MenuStat Project Repository

## Module Capabilities
This module is written and maintained to automate tasks related to the collection, cleaning, validation, and storage of nutrition data for the MenuStat database stewarded by Harvard University FAS Research Computing.


## Setup
To set up your environment for running the MenuStat module:
- **Set up conda.** The application uses conda for environment and dependency management. If you don't already have conda, install it and set it up. Instructions are available [here](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).

- **Create an environment.yaml file.** Use the file environment.yaml.example as a template.
- **Ensure that you have the latest version of Chrome installed.** Conda will download the latest release of Chromedriver. To use selenium, the Chromedriver version must match your Chrome browser version. If you update Chrome in the future, you'll also have to update this environment's Chromedriver. If chromedriver isn't compatible with your browser, you can still use the MenuStat package but no browser-based web scraping can occur.

## Using the Module
The primary purpose of this module is to automatically collect data for the franchises listed in the database's `franchises` table.

To review and update the contents of the database's `franchises` table:
1. Run the command `MenuStat.export_csv("2021_menustat_franchise_table.csv", "franchises")`
2. Update the franchise entries as needed (an overview of the process is available in the [manual](https://docs.google.com/document/u/1/d/e/2PACX-1vQ9VlcLYETZxMo6qCcp6gpvI9r0hjUHcEe6vRCtTss7d6wLcWyskBlCfdr9qdTGik2wYOhprV8rU7YH/pub).
3. Update the database table with the csv by running the command `MenuStat.import_csv("2021_menustat_franchise_table.csv", MenuStat.Franchise)`

To run the scraper on all franchises in the table, run:

    MenuStat.collect_and_enter_annualitemdata(dryrun=True)

To run the scraper on, for example, a franchise with the ID number 30, run:

    MenuStat.collect_and_enter_annualitemdata(dryrun=True, subset=30)

A few things to note about how this repository is set up:
- By default, the module first tries to open the csv of scraped data that corresponds to the franchise being updated. To see the scraping in action, delete the csv with the same number as the franchise_id in the *data* directory.
- The dfs_for_review are not used by the program. They're saved right before the database validation and entry steps and provide a way for a person to easily scan the data post-cleaning.


## Repository Overview
### Git Branches
This repository follows the git branching model outlined [here](https://nvie.com/posts/a-successful-git-branching-model/). The `master` branch is release-ready, and the `development` branch is the site of development. `Feature` branches are prefixed with `feature-`, `hotfix` branches with `hotfix-`.

### `menustat.db`
Test database containing the data needed to run the menustat module. db schema draft can be found [here](https://docs.google.com/presentation/d/1ym5Gv6MCgJUsTbstXfHZMqzhjQ7DV_SxK7LMlVB5cSY/edit#slide=id.gb87c4708b3_0_9).

### `menustat/`
This directory contains the parts of the menustat program which can be open-sourced.

#### `accessories.py`

#### `core.py`
core classes. Docstrings are available for all methods that are meant to be called directly by the user.

#### `utils.py`
Utility functions.


### `menustat/`
#### `menustat_module_usage_example.py`
Contains examples of different commands to run using the menustat module.

#### `nx_html.py`
A modification of pandas' html methods that menustat.py uses to collect nutritionix html table section notes separately from section titles.

#### `tests.py`
Unit testing module.

#### `testsuite`
Data used by test.py.


### `data/`
CSVs of scraped franchise menu and nutrition data. When inserting a franchise's annual item data into the database,  program tries to use data from the CSV with the name corresponding to the franchise's database ID. It only executes a scraping function if it fails to find one here.

### `jupyter_notebooks/`
Jupyter notebooks that combine code examples and tutorials for tasks such as identifying the correct way to process a particular pdf with the camelot library.
