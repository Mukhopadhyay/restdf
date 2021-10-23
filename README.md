# restdf

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=appveyor)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/2.0.x/)

[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

### Endpoints
|**Type**|**Method**|**Endpoint**|**Description**|**Request Body**|
|:-------|:---------|:------------|:--------------|:----------------|
|**Docs**|`GET`|`/`|||
|**Docs**|`GET`|`/stats`|||
|**Metadata**|`GET`|`/columns`|||
|**Metadata**|`POST`|`/describe`|||
|**Metadata**|`GET`|`/dtypes`|||
|**Metadata**|`GET`|`/info`|||
|**Metadata**|`GET`|`/nulls`|||
|**Metadata**|`GET`|`/value_counts/{column_name}`|||
|**Data**|`POST`|`/find_string/{column_name}`|||
|**Data**|`POST`|`/head`|||
|**Data**|`POST`|`/sample/{column_name}`|||
|**Data**|`POST`|`/isin/{column_name}`|||
|**Data**|`POST`|`/notin/{column_name}`|||
|**Data**|`POST`|`/equals/{column_name}`|||
|**Data**|`POST`|`/not_equals/{column_name}`|||
|**Data**|`POST`|`/values/{column_name}`|||
