# RestDF

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=appveyor)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/2.0.x/)

![Github Actions](https://github.com/Mukhopadhyay/restdf/actions/workflows/tests.yml/badge.svg)
[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Documentation Status](https://readthedocs.org/projects/restdf/badge/?version=latest)](https://restdf.readthedocs.io/en/latest/?badge=latest)

**RestDF** is a command line utility for running any `pandas.DataFrame` compatible datasets as a Rest API, with built-in `SwaggerUI` support.

* Source code: [https://github.com/Mukhopadhyay/restdf](https://github.com/Mukhopadhyay/restdf)
* License: [MIT](https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE)
* Documentation: [http://restdf.rtfd.io/](http://restdf.rtfd.io/)

### Geting Started with `RestDF`
The goal of this project was to make the API creation process from a dataset simpler. So, the execution is kept as minimal as possible. For example, <br/>
`RestDF` can be run like any other python module using the `-m` flag, additional flags can be used to configure the server.
Following will start a server with [this](https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv) dataset on [localhost:5000/docs](http://localhost:5000/docs)

```bash
python -m restdf https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv
```

For a more detailed description of all available flags and option please refer to this documentation on [Command Line Arguments](https://restdf.readthedocs.io/en/latest/pages/command-line-arguments.html).

### Endpoints

The responses from `RestDF` can be categorized into following three broad categories:
* `Docs`
* `Metadata`
* `Data`

Please refer to [this](https://restdf.readthedocs.io/en/latest/pages/endpoints.html) page for more detailed documentation on the available endpoints.

<br/>

### Testing:
**RestDF** tests are written using `pytest`. For more detailed documentation on testing this module please go to the following page: [Testing RestDF](https://restdf.readthedocs.io/en/latest/pages/tests.html)

### Documentations

Read the documentaion online at: [http://restdf.rtfd.io/](http://restdf.rtfd.io/)
Or build it locally from the `docs/` directory using

**Linux:**
```bash
make html
```
**Windows**
```bash
make.bat html
```
