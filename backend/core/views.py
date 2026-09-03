from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token


def auth_test(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
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
            "role": user.role.role_name,
        })

    if request.user.is_authenticated:
        return JsonResponse({
            "authenticated": True,
            "username": request.user.username,
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