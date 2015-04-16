import json
from django import template


from javascript_settings.configuration_builder import DEFAULT_CONFIGURATION_BUILDER


register = template.Library()

@register.tag(name='javascript_settings')
def do_javascript_settings(parser, token):
    """
        Returns a node with generated configuration.
    """
    return JavascriptConfigurationNode()


class JavascriptConfigurationNode(template.Node):
    """
        Represents a node that renders JavaScript configuration.
    """

    def __init__(self):
        pass

    def render(self, context):
        """
            Renders JS configuration.
        """
        js_code = """
        (function(){
            var configuration = %s;
            window.getDjangoParam = function(key){
                return configuration[key]
            };
        })();
        """

	if 'request' not in context:
            return ''

        return js_code % json.dumps(
                DEFAULT_CONFIGURATION_BUILDER.get_configuration(context['request'])
                )

