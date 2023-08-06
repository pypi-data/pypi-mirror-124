from setuptools import setup

VERSION = '1.0.1'
DESCRIPTION = 'Python scraper code to brainly website.'
LONG_DESCRIPTION = 'Python module to get questions and answers of "brainly.com", "brainly.com.br", "brainly.co.id" or "brainly.lat"\nExamples on github in English and Portuguese.'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="brainlypy", 
        version=VERSION,
        url='https://github.com/thiagopyy/brainlypy',
        project_urls ={
            'Source code':'https://github.com/thiagopyy/brainlypy'
        },
        license='MIT',
        author="thi.py",
        author_email="thidotpy@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['brainlypy'],
        install_requires=['requests', 'bs4'],
        keywords=['python', 'brainly', 'scraper'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
)