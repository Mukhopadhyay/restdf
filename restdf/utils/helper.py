import sys
import psutil

def get_index(filename: str) -> dict:
    INDEX_RESPONSE = {
        'filename': filename,
        'endpoints': [
            {
                'name': '/',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/stats',
                'type': ['GET'],
                'description': ''
            }
        ]
    }
    return INDEX_RESPONSE

def get_stats(framework:str, framework_version:str, stats_dict: dict) -> dict:
    vm = psutil.virtual_memory()
    stats = {
        'Server': {
            'name'   : framework,
            'version': framework_version,
        },
        'Python': {
            'version': sys.version,
        },
        'Runtime': {
            'filename'        : stats_dict.get('filename'),
            'runtime_duration': stats_dict.get('runtime_duration'),
            'running_since'   : stats_dict.get('running_since'),
            'API': {
                'total_requests'  : stats_dict.get('total_requests'),
                '/values_requests': stats_dict.get('values_requests'),
            }
        },
        'Device': {
            'cpu_percent': psutil.cpu_percent(),
            'Memory': {
                'total'    : vm.total,
                'available': vm.available,
                'percent'  : vm.percent,
                'used'     : vm.used,
                'free'     : vm.free
            }
        }
    }
    return stats
