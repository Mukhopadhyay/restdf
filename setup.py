# Built-in modules
import pathlib
# Third-party modules
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent
# The content of the README.md file
README = (HERE / "README.md").read_text()

# The setup method
setup(
    name='restdf',
    version='1.0.0',
    description='Create a simple API from a dataframe!',
    long_description=README,
    long_description_content_type='text/markdown',
    project_urls={
        'ReadTheDocs': 'https://restdf.readthedocs.io/en/latest/'
    },
    url='https://github.com/Mukhopadhyay/restdf',
    author='Pranesh Mukhopadhyay',
    author_email='praneshmukherjee7@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=['restdf',
              'restdf.configs',
              'restdf.routes',
              'restdf.routes.flask_schemas',
              'restdf.utils'],
    include_package_data=True,                          # Preemptively doing since, later MANIFEST.in will be added
    install_requires=[
        'flasgger==0.9.5',
        'Flask==2.0.2',
        'Flask-Cors==3.0.10',
        'numpy==1.21.3',
        'pandas==1.3.4',
        'psutil==5.8.0',
    ],
    entry_points={
        'console_scripts': [
            'restdf=restdf.__main__:main'
        ]
    }
)
