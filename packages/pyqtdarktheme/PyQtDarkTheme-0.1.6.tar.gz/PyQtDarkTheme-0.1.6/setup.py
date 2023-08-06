# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qdarktheme',
 'qdarktheme.dist',
 'qdarktheme.dist.dark',
 'qdarktheme.dist.light',
 'qdarktheme.qtpy',
 'qdarktheme.qtpy.QtCore',
 'qdarktheme.qtpy.QtGui',
 'qdarktheme.qtpy.QtSvg',
 'qdarktheme.qtpy.QtWidgets',
 'qdarktheme.widget_gallery',
 'qdarktheme.widget_gallery.ui']

package_data = \
{'': ['*'],
 'qdarktheme.dist.dark': ['svg/*'],
 'qdarktheme.dist.light': ['svg/*'],
 'qdarktheme.widget_gallery.ui': ['svg/*']}

setup_kwargs = {
    'name': 'pyqtdarktheme',
    'version': '0.1.6',
    'description': 'Flat dark theme for PySide, PyQt.',
    'long_description': 'PyQtDarkTheme\n=============\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pyqtdarktheme.svg?color=orange)](https://pypi.org/project/pyqtdarktheme/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pyqtdarktheme.svg?color=blue)](https://www.python.org/downloads/)\n[![Qt Versions](https://img.shields.io/badge/Qt-5%20|%206-blue.svg?&logo=Qt&logoWidth=18&logoColor=white)](https://www.qt.io/qt-for-python)\n[![License](https://img.shields.io/github/license/5yutan5/PyQtDarkTheme.svg?color=green)](https://github.com/5yutan5/PyQtDarkTheme/blob/main/LICENSE.txt/)\n[![Build Status](https://github.com/5yutan5/PyQtDarkTheme/workflows/os-test/badge.svg)](https://github.com/5yutan5/PyQtDarkTheme/actions/workflows/os-test.yml)\n[![CodeQL Status](https://github.com/5yutan5/PyQtDarkTheme/workflows/codeql/badge.svg)](https://github.com/5yutan5/PyQtDarkTheme/actions/workflows/code-quality.yml)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/5yutan5/PyQtDarkTheme.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/PyQtDarkTheme/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/5yutan5/PyQtDarkTheme.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/PyQtDarkTheme/context:python)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/python/black)\n\nDark theme for PySide and PyQt.\n\nPyQtDarkTheme applies a flat dark theme to Qt applications(PySide6, PyQt6, PyQt5 and PySide2) using the qt stylesheets system.\nThere\'s a Light Theme too. Color and style balanced from the Dark theme for easy viewing in daylight.\n\nPyQtDarkTheme is easy to freeze with freezing library(PyInstaller, py2app, cx_freeze or etc..).\n\n\n### Dark Theme\n![widget_gallery_dark_theme](https://raw.githubusercontent.com/5yutan5/PyQtDarkTheme/main/images/widget_gallery_dark.png)\n\n### Light Theme\n![widget_gallery_light_them](https://raw.githubusercontent.com/5yutan5/PyQtDarkTheme/main/images/widget_gallery_light.png)\n\n## Requirements\n\n- [Python 3.7+](https://www.python.org/downloads/)\n- PySide6, PyQt6, PyQt5 or PySide2\n\n## Installation Method\n\n- Last released version\n   ```plaintext\n   pip install pyqtdarktheme\n   ```\n- Latest development version\n   ```plaintext\n   pip install git+https://github.com/5yutan5/PyQtDarkTheme\n   ```\n\n## Usage\n\n```Python\nimport sys\n\nfrom PySide6.QtWidgets import QApplication, QMainWindow, QPushButton\n\nimport qdarktheme\n\napp = QApplication(sys.argv)\nmain_win = QMainWindow()\npush_button = QPushButton("PyQtDarkTheme!!")\nmain_win.setCentralWidget(push_button)\n\napp.setStyleSheet(qdarktheme.load_stylesheet())\n\nmain_win.show()\n\napp.exec()\n\n```\n\n> ⚠ The image quality may be lower on Qt5(PyQt5, PySide2) due to the use of svg. You can add the following attribute to improve the quality of images.\n> ```Python\n> app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)\n> ```\n\n### Light theme\n\n```Python\napp.setStyleSheet(qdarktheme.load_stylesheet("light"))\n```\n\n### Check common widgets\n\nTo check common widgets, run:\n\n```plaintext\npython -m qdarktheme.widget_gallery\n```\n\n## License\n\nPyQtDarkTheme incorporates image assets from external sources. The icons for the PyQtDarkTheme are derived [Material design icons](https://fonts.google.com/icons)(Apache License Version 2.0).\nAny file not listed in the [NOTICE.md](https://github.com/5yutan5/PyQtDarkTheme/blob/main/NOTICE.md) file is covered by PyQtDarkTheme\'s MIT license.\n',
    'author': 'Yunosuke Ohsugi',
    'author_email': '63651161+5yutan5@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/5yutan5/PyQtDarkTheme',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
