import importlib
import os
import sys

environment = os.environ.get('environment', 'local')
modules = ['base', environment]

if 'pytest' in sys.argv[0]:
    modules.append('test')

for module in modules:
    try:
        local_settings = importlib.import_module(f'config.{module}')
        globals().update(local_settings.__dict__)
    except ImportError:
        print(f'Failed to import settings.{module}')    # noqa
    else:
        if os.environ.get('DEBUG_SETTINGS'):
            print(f'Imported settings.{module}')    # noqa
