from typing import Dict, Any

flasgger_template: Dict[str, Any] = {
  "swagger": "2.0",
  "info": {
    "title": "RestDF API",
    "description": "<b>[Created using <code><a href='//github.com/Mukhopadhyay/restdf' target='_blank'>RestDF</a></code>]</b>",
    "contact": {
      "email": "praneshmukherjee7@gmail.com",
    },
    "termsOfService": "https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE",
    "version": "0.0.1"
  },
  "schemes": [
    "http"
  ]
}

flasgger_config = {
    'headers': [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
