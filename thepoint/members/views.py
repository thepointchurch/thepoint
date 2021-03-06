# pylint: disable=too-many-ancestors

import logging
import platform
import sys
from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ..directory.models import Person
from ..roster.models import Role
from ..utils.mixin import NeverCacheMixin, VaryOnCookieMixin

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata  # pylint: disable=no-name-in-module
else:
    import importlib_metadata


logger = logging.getLogger(__name__)


class IndexView(VaryOnCookieMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = "members/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["role_list"] = (
                Role.current_objects.filter(people__id=self.request.user.person.id)
                .filter(meeting__date__lte=(date.today() + timedelta(days=60)))
                .select_related("meeting", "role", "location",)
                .prefetch_related("people", "people__family",)
                .only(
                    "description",
                    "meeting__date",
                    "role__name",
                    "location__name",
                    "people__name",
                    "people__suffix",
                    "people__surname_override",
                    "people__family__name",
                )
            )
        except Exception:  # pylint: disable=broad-except
            pass
        context["webmaster_email"] = settings.WEBMASTER_EMAIL
        context["search_query"] = ""
        context["person"] = getattr(self.request.user, "person", None)
        return context


def not_a_guest(user):
    try:
        return user.is_authenticated and (user.is_staff or user.person)
    except Exception as exc:
        raise PermissionDenied from exc


class CreateView(NeverCacheMixin, LoginRequiredMixin, generic.ListView):
    model = Person
    template_name = "members/create_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query", "")
        return context

    def get_queryset(self):
        query = self.request.GET.get("query", "")

        if query == "":
            return Person.current_objects.none()
        return (
            Person.current_objects.filter(user__isnull=True)
            .filter(Q(name__icontains=query) | Q(surname_override__icontains=query) | Q(family__name__icontains=query))
            .distinct()
            .only("name", "suffix", "surname_override", "family__name")
        )


class CreateConfirmView(NeverCacheMixin, LoginRequiredMixin, generic.edit.CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "members/create_form.html"
    success_url = reverse_lazy("members:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["person"] = get_object_or_404(
            Person.current_objects.select_related("family").only("name", "suffix", "surname_override", "family__name"),
            pk=self.kwargs.get(self.pk_url_kwarg, None),
        )
        return context

    def post(self, request, *args, **kwargs):
        person = get_object_or_404(Person, pk=self.kwargs.get(self.pk_url_kwarg, None))

        try:
            self.model.objects.get(username=request.POST["username"])
            messages.error(request, _("A user with that username already exists."))
            return redirect(request.path)
        except self.model.DoesNotExist:
            pass

        if request.POST["password1"] != request.POST["password2"]:
            messages.error(request, _("The two password fields didn't match."))
            return redirect(request.path)

        result = super().post(request, *args, **kwargs)

        if not self.object:
            logger.error("Error creating user %r", self.object)
            messages.error(request, _("An error occurred trying to create your account."))
            return redirect(request.path)

        person.user = self.object
        person.save()

        # slight hack to log in as the new user
        logout(request)
        self.object.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, self.object)

        messages.success(request, _("Your account has been set up successfully."))

        return result


class TechDetailsView(NeverCacheMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = "members/tech_details.html"

    def get_context_data(self, **kwargs):
        key_map = {
            __name__.split(".")[0]: 0,
            "Django": 1,
        }

        context = super().get_context_data(**kwargs)
        context["python_version"] = sys.version
        context["platform"] = platform.platform()
        context["packages"] = [
            {
                "name": dist.metadata["Name"],
                "version": dist.version,
                "url": dist.metadata.get("Home-page"),
                "key": (key_map.get(dist.metadata["Name"], 99), dist.metadata["Name"]),
            }
            for dist in importlib_metadata.distributions()
        ]
        return context
