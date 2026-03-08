# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import datetime
import sys
from pathlib import Path
from contextlib import suppress

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MCDR-Plugins'
copyright = f'{datetime.datetime.now().year}, xieyuen'
author = 'xieyuen'
release = '0.1.0'

src = Path(__file__).parent.parent.parent / "src"
dependencies = Path(__file__).parent.parent.parent / "dependencies"

for directory in src.iterdir():
    sys.path.append(str(directory))

with suppress(FileNotFoundError):
    for directory in dependencies.iterdir():
        sys.path.append(str(directory))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
    'sphinx_prompt',

    # For codeblock tabs
    # https://github.com/pradyunsg/sphinx-inline-tabs
    'sphinx_inline_tabs',

    # Mermaid graphs
    # https://github.com/mgaitan/sphinxcontrib-mermaid
    'sphinxcontrib.mermaid',

    # https://sphinx-design.readthedocs.io/en/latest/index.html
    # 'sphinx_design',

    # https://pypi.org/project/sphinxcontrib.asciinema/
    'sphinxcontrib.asciinema'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- extension configuations -------------------------------------------------

# 常用的外部文档链接映射
# intersphinx_mapping = {
#     'python': ('https://docs.python.org/3', None),
#     'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
#     'mcdr': ('https://mcdreforged.com', None)
# }
autodoc_default_options = {
    'members': True,           # 显示所有成员
    'member-order': 'bysource', # 按源代码顺序
    'special-members': '__init__',  # 显示特殊方法
    'undoc-members': True,      # 显示没有文档的成员
    'show-inheritance': True,   # 显示继承关系
}