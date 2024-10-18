class CacheControlMiddleware:
    """
    https://stackoverflow.com/questions/49220992/how-to-disable-ie11-cache-in-django-rest
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache'
        return response
