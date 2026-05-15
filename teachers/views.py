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

# Create your views here.
