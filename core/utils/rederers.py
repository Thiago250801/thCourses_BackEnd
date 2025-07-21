from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Customize the response data here
        response = renderer_context.get('response', None)
        
        success = True
        
        if response is not None and response.status_code >= 400:
            success = False
        # If data is None, we set it to an empty object       
        response_data = {
            'success': success,
            'data': data if data is not None else {}
        }
        
        if "detail" in data:
            response_data['detail'] = data['detail']
            
        if "success" in data:
            del data['success']

        return super().render(response_data, accepted_media_type, renderer_context)