from django.shortcuts import redirect, render


def login_page(request):
    """Display the ERA-IPMS login page."""
    return render(request, "core/login.html")


def dashboard_page(request):
    """Display the protected ERA-IPMS dashboard."""
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "core/dashboard.html")
