from django.contrib.auth import get_user_model

class DemoUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            User = get_user_model()
            demo_user, created = User.objects.get_or_create(username='demo_user')
            request.user = demo_user
        return self.get_response(request)
