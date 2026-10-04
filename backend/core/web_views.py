from django.shortcuts import render


def login_page(request):
    """Display the ERA-IPMS login page."""
    return render(request, "core/login.html")
