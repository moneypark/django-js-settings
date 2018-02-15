import json
from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.template import Template, Context

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

    # We need to render JS settings as an escaped string first to avoid issues with HTML injections.
    # HTML is parsed before JavaScript, therefore we cannot allow unescaped HTML-tags.
    js_template_str = """
    (function(){
        var json_string = '{{ js_configuration|escapejs }}';
        var configuration = JSON.parse(json_string);
        window.getDjangoParam = function(key){
            return configuration[key]
        };
    })();
    """

    def __init__(self):
        pass

    def render(self, context):
        """
            Renders JS configuration.
        """
        if 'request' not in context:
            return ''

        js_template = Template(self.js_template_str)
        template_context = Context({
            'js_configuration': json.dumps(
                DEFAULT_CONFIGURATION_BUILDER.get_configuration(context['request']),
                cls=DjangoJSONEncoder
            ),
        })
        return js_template.render(template_context)
