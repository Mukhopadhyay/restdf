from typing import Dict, Any

flasgger_config: Dict[str, Any] = {
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
