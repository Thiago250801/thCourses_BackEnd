from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler to return a more user-friendly error response.
    """
    response = exception_handler(exc, context)

    ## Manter um padrão de resposta para erros
    if response is not None:
        if response.data.get('messages'):
            del response.data['messages']
            
        if response.data.get('success') is None:
            response.data['success'] = False
    
    return response