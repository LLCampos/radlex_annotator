try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='radlex_annotator',
    version='0.1',
    packages=['annotator'],
    description="A local NCBO Annotator replacement to annotate RadLex terms.",
    author='Lu\xc3\xads Campos',
    author_email='luis.filipe.lcampos@gmail.com',
    url='https://github.com/LLCampos/radlex_annotator',
    license='',
    include_package_data=True,
    install_requires=[
        'lxml'
    ],
)
