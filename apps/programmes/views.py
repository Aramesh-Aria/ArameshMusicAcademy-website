from django.views.generic import DetailView

from .models import Programme


class ProgrammeDetailView(DetailView):
    template_name = 'programmes/programme_detail.html'
    context_object_name = 'programme'

    def get_queryset(self):
        return Programme.objects.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_description'] = ' '.join(self.object.short_description.split())[:160]
        return context
