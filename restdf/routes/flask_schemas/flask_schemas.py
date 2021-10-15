openapi_format = {
    'summary': None,
    'description': None,
    'tags': None,
    'produces': 'application/json'
}
column_name_param = {
    'name': 'column_name',
    'in': 'path',
    'type': 'string',
    'enum': None,
    'required': 'true',
    'default': None
}
flask_response_schema = {
    '200': {
        'description': None,
        'schema': {
            'type': 'object',
            'example': None
        }
    }
}

specs_dict = {
    "parameters": [
        {
            "name": "palette",
            "in": "path",
            "type": "string",
            "enum": [
                "all",
                "rgb",
                "cmyk"
            ],
            "required": "true",
            "default": "all"
        }
    ],
    "definitions": {
        "Palette": {
            "type": "object",
            "properties": {
                "palette_name": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Color"
                    }
                }
            }
        },
        "Color": {
            "type": "string"
        }
    },
    "responses": {
        "200": {
            "description": "A list of colors (may be filtered by palette)",
            "schema": {
                "$ref": "#/definitions/Palette"
            },
            "examples": {
                "rgb": [
                    "red",
                    "green",
                    "blue"
                ]
            }
        }
    }
}