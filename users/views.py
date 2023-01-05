from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from users.forms import CreateUserForm, LoginUserForm
from typing import Any


class Login(LoginView):
    template_name: str = "auth/login.dj.html"
    authentication_form: Any = LoginUserForm
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("profile")


class Logout(LogoutView):
    next_page: str = "login"
    template_name: str = "auth/logout.dj.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.render_to_response(self.get_context_data())
        else:
            return redirect("login")

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(
                self.request, messages.SUCCESS, "Logged out successfully"
            )
            return super().post(request, *args, **kwargs)
        else:
            return redirect("login")


def register(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Account created successfully"
            )
            return redirect("login")
        else:
            return render(request, "auth/register.dj.html", {"form": form})
    else:
        form = CreateUserForm()

    return render(request, "auth/register.dj.html", {"form": form})
