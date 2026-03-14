# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import datetime
import sys
from pathlib import Path
from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MCDR-Plugins'
copyright = f'{datetime.datetime.now().year}, xieyuen'
author = 'xieyuen'
release = '1.0.0'

repo_root = Path(__file__).parent.parent.parent
src = repo_root / "src"
dependencies = repo_root / "dependencies"

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

templates_path = ['../templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['../static']
html_css_files = ['custom.css']

# -- extension configuations -------------------------------------------------

# 常用的外部文档链接映射
intersphinx_mapping = {
    'mcdreforged': ('https://docs.mcdreforged.com/zh-cn/latest/', None),
    'python': ('https://docs.python.org/3', None),
}

# -- Options for sphinx.ext.autodoc -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_member_order = 'bysource'
autodoc_inherit_docstrings = False  # so overridden methods won't pop up
autodoc_default_options = {
    'members': True,           # 显示所有成员
    'special-members': '__init__',  # 显示特殊方法
    'undoc-members': True,      # 显示没有文档的成员
    'show-inheritance': True,   # 显示继承关系
}

# -- Options for sphinx.ext.autosectionlabel -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
autosectionlabel_prefix_document = True


# 删除线样式
rst_prolog = """
.. role:: del
    :class: del
"""
