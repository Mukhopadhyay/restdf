# RestDF

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=appveyor)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/2.0.x/)

[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**RestDF** is a command line utility for running any `pandas.DataFrame` compatible datasets as a Rest API, with built-in `SwaggerUI` support.

* Source code: [https://github.com/Mukhopadhyay/restdf](https://github.com/Mukhopadhyay/restdf)
* License: [MIT](https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE)

### Running `RestDF`

`RestDF` can be run like any other python module using the `-m` flag, additional flags can be used to configure the server.
Following will start a server with [this](https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv) dataset on [localhost:5000/docs](http://0.0.0.0:5000/docs)

```bash
python -m restdf https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv
```
### Command line arguments:

|**Type**|**Flag**|**Expected Dtype**|**Description**|**example**|
|:-------|:-------|:-----------------|:--------------|:----------|
|MANDATORY||`str`|Path to the dataset|`restdf ./path/to/dataset.csv`|
|OPTIONAL|`-H`, `--host`|`str`|**Host** for the Flask server|`restdf data.csv -H 0.0.0.0`|
|OPTIONAL|`-p`, `--port`|`int`|**Port** on which to run the server|`restdf data.csv -p 8080`|
|OPTIONAL|`-d`, `-debug`|`bool`|Wheather to run the server on [debug](https://flask.palletsprojects.com/en/2.0.x/debugging/) mode|`restdf data.csv -d`|
|OPTIONAL|`-t`, `--title`|`str`|Name of the server on `SwaggerUI`|`restdf data.csv -t "Test API"`|
|OPTIONAL|`-e`, `--email`|`str`|Developer email on `SwaggerUI`|`restdf data.csv -e email@email.com`|

Using all of these options our command would look something like this
```bash
python -m restdf https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv --host 0.0.0.0 --port 5555 -d -t "Diamonds Dataset" -e "username@email.com"
```
this would run start the server on the port number `5555`.

### Endpoints

The responses from `RestDF` are broken into three fundamental types
* `Docs`<br/>
These endpoints provides some documentation on the API. Following are the available documentation related endpoints.

|**Type**|**Method**|**Endpoint**|**Description**|
|:-------|:---------|:-----------|:--------------|
|**Docs**|`GET`|`/`|Index route, gives brief intro about the API|
|**Docs**|`GET`|`/docs`|`SwaggerUI`|
|**Docs**|`GET`|`/stats`|Provides basic Stats about the currently running API|


* `Metadata`<br/>
As the name suggests, these provide some information about the dataset itself.

|**Type**|**Method**|**Endpoint**|**Description**|
|:-------|:---------|:-----------|:--------------|
|**Metadata**|`GET`|`/columns`|Get the dataframe columns|
|**Metadata**|`POST`|`/describe`|Describes different properties of the dataframe|
|**Metadata**|`GET`|`/dtypes`|Returns the datatype of all columns|
|**Metadata**|`GET`|`/info`|Returns some dataframe info (Datatype, Non-null counts etc)|
|**Metadata**|`GET`|`/nulls`|Returns the count of nulls in the dataframe|
|**Metadata**|`GET`|`/value_counts/{column_name}`|Returns the value_count results of a column|

* `Data`<br/>
These endpoints returns values from the dataset.

|**Type**|**Method**|**Endpoint**|**Description**|
|:-------|:---------|:-----------|:--------------|
|**Data**|`POST`|`/equals/{column_name}`|Returns rows where all column values are exactly equal to the given value|
|**Data**|`POST`|`/find_string/{column_name}`|Returns rows where all string values contains given pattern|
|**Data**|`POST`|`/head`|Returns the head of the dataframe|
|**Data**|`POST`|`/isin/{column_name}`|Returns rows where all column values are within the array content|
|**Data**|`POST`|`/not_equals/{column_name}`|Returns rows where all column values are not equal to the given value|
|**Data**|`POST`|`/notin/{column_name}`|Returns rows where all column values are not within the array content|
|**Data**|`POST`|`/sample/{column_name}`|Returns random rows from the dataframe|
|**Data**|`POST`|`/values/{column_name}`|Returns values for a selected column|


<br/>

### Testing:
**RestDF** tests are written using `pytest`,
```bash
pytest -v
```
The available pytest `markers` are:
|**Name**|**Description**|
|:-------|:--------------|
|`io`|File input-output related tests|
|`flask`|All Flask related tests|
|`routes`|All endpoint related tests|
|`utils`|Testing all utility scripts|