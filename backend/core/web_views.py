from django.shortcuts import redirect, render


def login_page(request):
    """Display the ERA-IPMS login page."""
    return render(request, "core/login.html")


def dashboard_page(request):
    """Display the protected ERA-IPMS dashboard."""
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "core/dashboard.html")



def projects_page(request):
    """Display the protected Projects page."""
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "core/projects.html")



def beneficiaries_page(request):
    """Display the protected Beneficiary Services page."""
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "core/beneficiaries.html")



def poultry_page(request):
    """Display the protected Poultry page."""
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "core/poultry.html")



def farm_page(request):
    """Display the protected Small Farm page."""
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "core/farm.html")
