# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['savefigs']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0']

setup_kwargs = {
    'name': 'savefigs',
    'version': '0.2.0',
    'description': 'Save all open Matplotlib figures',
    'long_description': '# savefigs\n\n[![CI workflow status](https://github.com/zmoon/savefigs/actions/workflows/ci.yml/badge.svg)](https://github.com/zmoon/savefigs/actions/workflows/ci.yml)\n[![Version on PyPI](https://img.shields.io/pypi/v/savefigs.svg)](https://pypi.org/project/savefigs/)\n\nEasily save all open Matplotlib figures, with useful filenames.\n\n## Usage\n\n*Assume we have a script `some_script.py` that creates multiple Matplotlib figures.*\n\nImport the `savefigs` function:\n```python\nfrom savefigs import savefigs\n```\n\nThe below examples assume the figures do not have labels (`fig.get_label()`).\nIf a figure does have a label, it will be used in place of `fig{num}`.\n\nDefault save settings (`./{script filename stem}{figure label or fig{num}}.png`):\n```python\nsavefigs()\n# ./some_script_fig1.png, ./some_script_fig2.png, ...\n```\n👆 The filenames tell us which script generated the figures as well as their relative places in the figure generation order (or labels if they are labeled).\n\nSpecify directory:\n```python\nsavefigs(save_dir="figs")  # must exist\n# ./figs/some_script_fig1.png, ./figs/some_script_fig2.png, ...\n```\n\nSpecify a different prefix to the base stem format:\n```python\nsavefigs(stem_prefix="run1")\n# ./run1_fig1.png, ./run1_fig2.png, ...\n```\n\nSave in multiple file formats:\n```python\nsavefigs(formats=["png", "pdf"])\n# ./some_script_fig1.png, ./some_script_fig1.pdf, ...\n```\n\nAvoid overwriting files:\n```python\nsavefigs(clobber=False, noclobber_method="add_num")\n# ./some_script_fig3.png (assuming ./some_script_fig{1,2}.png already exist)\n```\n👆 By default (without changing `noclobber_method`), setting `clobber=False` will instead error.\n\n## Background\n\nWhen writing a script that creates multiple figures, I usually label them (usually using the `num` argument to `plt.figure()`/`plt.subplots()`), which makes it easier to find the correct figure window. Then, at the end of the script I write a loop like:\n```python\nfor num in plt.get_fignums():\n    fig = plt.figure(num)\n    fig.savefig(f"{fig.get_label()}.pdf", ...)\n    # Maybe another format...\n```\n`savefigs()` essentially does this, but is more robust and provides additional features through keyword arguments. And it saves having to write those lines in the script, instead allowing the simple one-liner:\n```python\nfrom savefigs import savefigs; savefigs()\n```\n',
    'author': 'zmoon',
    'author_email': 'zmoon92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zmoon/savefigs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
