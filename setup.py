"""
setup.py file for pysweeper package
"""
import setuptools

dependencies = [ 'emoji', 'colorama' ]

setuptools.setup(
    name="pysweeper",
    version="1.0.1",
    author="Maarten J Broekman",
    url="https://github.com/mjbroekman/python-minesweeper",
    description="CLI MineSweeper game",
    license="GPL-3.0 - https://opensource.org/licenses/GPL-3.0",
    package_dir={'':'src/pysweeper'}
)
