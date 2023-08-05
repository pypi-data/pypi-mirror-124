# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datahints']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datahints',
    'version': '0.1.1',
    'description': 'Type hinting for pandas DataFrame',
    'long_description': '# datahints\n\nValidate pandas dataframes using type information.\nEnables IDE autocompletion and refactoring of column names\nas well as explicitly documenting expected columns and their data types.\n\nAll dataframes are treated as standard pandas dataframes,\nno instancing of the subclasses is required.\n\n## Installation\n`pip install datahints`\n\n## Example\n```python\nimport pandas as pd\nimport numpy as np\nfrom datahints import DataFrame, Series\nfrom typing import Optional, Union\n\nclass MyDataFrame(DataFrame):\n    col1: Series[int]\n    col2: Series[Union[int, float]]\n    col3: Optional[Series[np.float64]]\n\n# validate any dataframe\ndf = pd.DataFrame({"col1": [1, 2], "col2": [3.0, 4.0]})\nMyDataFrame.validate(df)\n\n# validate and annotate type for IDE support\ndf = MyDataFrame.validate(df)\n\n# use statically named columns \ndf[MyDataFrame.col3] = [5.0, 6.0]\n\n# constructor simply returns a dataframe instance\ndf = MyDataFrame({MyDataFrame.col1: [1, 2], MyDataFrame.col2: [3.0, 4.0]})\nMyDataFrame.validate(df)\n\n# create and validate directly\ndf = MyDataFrame.create({\n    MyDataFrame.col1: [1, 2],\n    MyDataFrame.col2: [3.0, 4.0]\n})\n\n# infer column names automatically (if all columns are present)\ndf = MyDataFrame.create([\n    (1, 3.0, 5.0),\n    (2, 4.0, 6.0)\n])\n```\n\n## Type inference\nNative types are automatically assumed to represent the following numpy equivalents:\n\n|type|dtype|\n|----|-----|\n|`str`|`np.str_`, `np.object_`|\n|`int`|`np.int32`, `np.int64`|\n|`float`|`np.float32`, `np.float64`|\n|`bool`|`np.bool_`|\n|`date`, `datetime`|`"datetime64[ns]"`|\n',
    'author': 'Ketil Albertsen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/litek/datahints',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
