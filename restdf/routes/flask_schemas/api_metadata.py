flask_api_metadata = {
    '/value_counts/<column_name>': {
        'summary': "Value counts, returns frequently occurring elements of a column",
        'description': "This endpoint returns the response from <code>series.value_counts()</code> & returns the result.",
        'tags': ['Metadata'],
        'consumes': ['application/text'],
        'produces': ['application/json'],
        'responses': {
            '200': {
                'description': 'Success',
                'schema': {
                    'type': 'object',
                    'example': {"column": "SibSp", "value_counts": {"0": 19, "1": 8, "2": 1, "4": 1, "5": 1}}
                }
            }
        }
    }
}
