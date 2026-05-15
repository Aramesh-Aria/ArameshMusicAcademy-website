from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'subject',
        'message_preview',
        'is_read',
        'created_at',
    )
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'
    actions = ('mark_as_read', 'mark_as_unread')
    fieldsets = (
        ('اطلاعات فرستنده', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('پیام', {
            'fields': ('subject', 'message', 'is_read')
        }),
        ('تاریخ', {
            'fields': ('created_at',)
        }),
    )

    @admin.display(description='خلاصه پیام')
    def message_preview(self, obj):
        if len(obj.message) <= 50:
            return obj.message
        return f'{obj.message[:50]}...'

    @admin.action(description='علامت‌گذاری به عنوان خوانده شده')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='علامت‌گذاری به عنوان خوانده نشده')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

# Register your models here.
