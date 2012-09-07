class JavaScriptUserConfig(object):
    """ 
        Adds abbility to add parameters to javascript_settings
        from view.
        
        Example:
            request.javascript_settings.update({'foo': 'bar'})
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.javascript_settings = {}