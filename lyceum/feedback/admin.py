__all__ = ()

import django.contrib.admin

import feedback.models


class FeedbackFileInline(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackFile
    extra = 0
    readonly_fields = (feedback.models.FeedbackFile.file.field.name,)


class StatusLogInline(django.contrib.admin.TabularInline):
    model = feedback.models.StatusLog
    extra = 0
    readonly_fields = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to.field.name,
        feedback.models.StatusLog.timestamp.field.name,
    )
    can_delete = False


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        "get_name",
        "get_mail",
        feedback.models.Feedback.status.field.name,
    )
    inlines = [FeedbackFileInline, StatusLogInline]

    @django.contrib.admin.display(description="Имя")
    def get_name(self, obj):
        return obj.personal_data.name if obj.personal_data else "-"

    @django.contrib.admin.display(description="Почта")
    def get_mail(self, obj):
        return obj.personal_data.mail if obj.personal_data else "-"

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = feedback.models.Feedback.objects.get(pk=obj.pk)
            status_field_name = feedback.models.Feedback.status.field.name
            if getattr(old_obj, status_field_name) != getattr(
                obj,
                status_field_name,
            ):
                feedback.models.StatusLog.objects.create(
                    user=request.user,
                    feedback=obj,
                    from_status=getattr(old_obj, status_field_name),
                    to=getattr(obj, status_field_name),
                )

        super().save_model(request, obj, form, change)


@django.contrib.admin.register(feedback.models.StatusLog)
class StatusAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to.field.name,
        feedback.models.StatusLog.timestamp.field.name,
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
