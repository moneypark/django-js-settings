import sys

from javascript_settings import settings
from copy import deepcopy


class ConfigurationBuilder:
    """
        Get javascript configurations from urls.py files from all installed apps.
    """
    def __init__(self):
        self.configuration = None

    def fetch(self):
        configuration = {}
        for app_name, module_name in settings.SCAN_MODULES.items():
            try:
                __import__(module_name)
                urls = sys.modules[module_name]
                if hasattr(urls, 'javascript_settings'):
                    configuration[app_name] = urls.javascript_settings()
            except ImportError:
                pass
        return configuration

    def get_configuration(self, request=None):
        if self.configuration is None:
            self.configuration = self.fetch()

        configuration = deepcopy(self.configuration)
        # Get configuration for current view
        if request and hasattr(request, 'javascript_settings'):
            configuration.update(request.javascript_settings)

        return configuration

DEFAULT_CONFIGURATION_BUILDER = ConfigurationBuilder()
