from django.views.generic import DetailView, ListView

from .models import Teacher


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        return (
            Teacher.objects
            .filter(is_active=True)
            .prefetch_related('instruments')
        )


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'

    def get_queryset(self):
        return (
            Teacher.objects
            .filter(is_active=True)
            .prefetch_related('instruments')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        if teacher.biography:
            context['meta_description'] = ' '.join(teacher.biography.split())[:160]
        else:
            instruments = '، '.join(i.name for i in teacher.instruments.all())
            context['meta_description'] = (
                f'{teacher.full_name} مدرس {instruments} در آموزشگاه موسیقی آرامش.'
            )
        context['teacher_sessions'] = (
            teacher.class_sessions
            .filter(is_active=True)
            .prefetch_related('instruments')
            .order_by('weekday_order', 'start_time')
        )
        return context
