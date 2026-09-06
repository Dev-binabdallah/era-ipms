from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token


def auth_test(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=identifier,
            password=password,
        )

        if user is None:
            return JsonResponse(
                {"authenticated": False},
                status=401,
            )

        login(request, user)

        return JsonResponse({
            "authenticated": True,
            "user_id": user.user_id,
            "username": user.username,
            "title": user.title.title_name,
        })

    if request.user.is_authenticated:
        return JsonResponse({
            "authenticated": True,
            "user_id": request.user.user_id,
            "username": request.user.username,
            "title": request.user.title.title_name,
        })

    get_token(request)

    return JsonResponse({
        "authenticated": False,
    })


def auth_logout(request):
    logout(request)

    return JsonResponse({
        "authenticated": False,
        "message": "Logged out successfully",
    })
