# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['utility_bill_scraper',
 'utility_bill_scraper.bin',
 'utility_bill_scraper.canada.on']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.0,<2.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'google-api-python-client>=2.27.0,<3.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'pdfminer>=20191125,<20191126',
 'python-dotenv>=0.19.1,<0.20.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'utility-bill-scraper',
    'version': '0.5',
    'description': 'Utility bill scraper for extracting data from pdfs and websites.',
    'long_description': '<!-- #region tags=[] -->\n# Utility bill scraper\n\n[![build](https://github.com/ryanfobel/utility-bill-scraper/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/ryanfobel/utility-bill-scraper/actions/workflows/build.yml)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ryanfobel/utility-bill-scraper/main)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/utility-bill-scraper.svg)](https://pypi.python.org/pypi/utility-bill-scraper/)\n\nDownload energy usage and carbon emissions data from utility websites or pdf bills.\n\n## Supported utilities\n\nThe simplest way to get started without installing anything on your computer is to click on one of the following links, which will open a session on https://mybinder.org where you can try downloading some data.\n\n * [Kitchener Utilities (gas & water)](https://mybinder.org/v2/gh/ryanfobel/utility-bill-scraper/main?labpath=notebooks%2Fcanada%2Fon%2Fkitchener_utilities.ipynb)\n \n## Install\n\n```sh\npip install utility-bill-scraper\n```\n<!-- #endregion -->\n\n<!-- #region -->\n## Get updates\n\n```python\nimport utility_bill_scraper.canada.on.kitchener_utilities as ku\n\nku_api = ku.KitchenerUtilitiesAPI(username, password)\n\n# Get new statements.\nupdates = ku_api.update()\nif updates is not None:\n    print(f"{ len(updates) } statements_downloaded")\nku_api.history().tail()\n```\n![history tail](https://raw.githubusercontent.com/ryanfobel/utility-bill-scraper/main/notebooks/canada/on/images/history_tail.png)\n<!-- #endregion -->\n\n<!-- #region -->\n## Plot monthly gas consumption\n\n```python\ndf_ku = ku_api.history()\n\nplt.figure()\nplt.bar(df_ku.index, df_ku["Gas Consumption"], width=bin_width, alpha=alpha)\nplt.xticks(rotation=90)\nplt.title("Monthly Gas Consumption")\nplt.ylabel("m$^3$")\n```\n![monthly gas consumption](https://raw.githubusercontent.com/ryanfobel/utility-bill-scraper/main/notebooks/canada/on/images/monthly_gas_consumption.svg)\n<!-- #endregion -->\n\n<!-- #region -->\n## Convert gas consumption to CO2 emissions\n\n```python\nfrom utility_bill_scraper import GAS_KGCO2_PER_CUBIC_METER\n\ndf_ku["kgCO2"] = df_ku["Gas Consumption"] * GAS_KGCO2_PER_CUBIC_METER\n```\n<!-- #endregion -->\n\n<!-- #region -->\n## Plot CO2 emissions versus previous years\n\n```python\nn_years_history = 1\n\nplt.figure()\nfor year, df_year in df_ku.groupby("year"):\n    if year >= dt.datetime.utcnow().year - n_years_history:\n        df_year.sort_values("month", inplace=True)\n        plt.bar(\n            df_year["month"],\n            df_year["Gas Consumption"],\n            label=year,\n            width=bin_width,\n            alpha=alpha,\n        )\nplt.legend()\nplt.ylabel("m$^3$")\nplt.xlabel("Month")\nylim = plt.ylim()\nax = plt.gca()\nax2 = ax.twinx()\nplt.ylabel("tCO$_2$e")\nplt.ylim([GAS_KGCO2_PER_CUBIC_METER * y / 1e3 for y in ylim])\nplt.title("Monthly CO$_2$e emissions from natural gas")\n```\n![monthly_co2_emissions](https://raw.githubusercontent.com/ryanfobel/utility-bill-scraper/main/notebooks/canada/on/images/monthly_co2_emissions.svg)\n<!-- #endregion -->\n\n<!-- #region -->\n## Command line utilities\n\nUpdate and export your utility data from the command line.\n\n### Update data\n\n```sh\n> python -m utility_bill_scraper.bin.ubs --utilty-name "Kitchener Utilities" update --user $USER --password $PASSWORD\n```\n\n### Export data\n\n```sh\n> python -m utility_bill_scraper.bin.ubs --utilty-name "Kitchener Utilities" export --output data.csv\n```\n\n### Options\n\n```sh\n> python -m utility_bill_scraper.bin.ubs --help\nusage: ubs.py [-h] [-e ENV] [--data-path DATA_PATH] [--utility-name UTILITY_NAME]\n              [--google-sa-credentials GOOGLE_SA_CREDENTIALS]\n              {update,export} ...\n\nubs (Utility bill scraper)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -e ENV, --env ENV     path to .env file.\n  --data-path DATA_PATH\n                        folder containing the history file\n  --utility-name UTILITY_NAME\n                        name of the utility\n  --google-sa-credentials GOOGLE_SA_CREDENTIALS\n                        google service account credentials\n\nsubcommands:\n  {update,export}       available sub-commands\n```\n\n### Environment variables\n\nNote that many options can be set via environment variables (useful for continuous integration and/or working with containers). The following can be set in your shell or via a `.env` file passed using the `-e` option.\n\n```sh\nDATA_PATH\nUTILITY_NAME\nGOOGLE_SA_CREDENTIALS\nUSER\nPASSWORD\nSAVE_STATEMENTS\nMAX_DOWNLOADS\n```\n\n## Contributors\n\n* [Ryan Fobel](https://github.com/ryanfobel)\n<!-- #endregion -->\n\n```python\n\n```\n',
    'author': 'Ryan Fobel',
    'author_email': 'ryan@fobel.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
