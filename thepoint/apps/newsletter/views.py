from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Issue, Publication


class PublicationMixin(UserPassesTestMixin):
    def test_func(self):
        self.publication = get_object_or_404(
            Publication,
            slug=self.request.resolver_match.namespace)
        return (not self.publication.is_private or
                self.request.user.is_authenticated)


class IndexView(PublicationMixin, generic.ListView):
    template_name = 'newsletter/index.html'
    paginate_by = 10

    def get_queryset(self):
        return self.publication.issues.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['publication'] = self.publication
        return context


class DetailView(PublicationMixin, generic.DetailView):
    model = Issue

    def get_queryset(self):
        return self.publication.issues.all()

    def get(self, request, *args, **kwargs):
        issue = self.get_object()

        if getattr(default_storage, 'offload', False):
            disposition = ('attachment; filename="%s %s%s"' % (
                           issue.publication.name,
                           issue.date,
                           issue.extension,
                           ))
            response_headers = {
                'response-content-disposition': disposition,
                'response-content-type':        issue.mime_type,
            }
            response = HttpResponseRedirect(
                default_storage.url(issue.file.name,
                                    response_headers=response_headers))
        else:
            response = HttpResponse(issue.file, content_type=issue.mime_type)
            response['Content-Disposition'] = (
                ('attachment; filename="%s %s%s"' % (
                 issue.publication.name,
                 issue.date,
                 issue.extension,
                 )))
        return response