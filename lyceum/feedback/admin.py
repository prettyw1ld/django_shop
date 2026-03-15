__all__ = ()

import django.contrib.admin

from feedback.models import Feedback, StatusLog


@django.contrib.admin.register(Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "mail", "status")

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Feedback.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                StatusLog.objects.create(
                    user=request.user,
                    feedback=obj,
                    from_status=old_obj.status,
                    to_status=obj.status,
                )

        super().save_model(request, obj, form, change)


@django.contrib.admin.register(StatusLog)
class StatusAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("user", "from_status", "to")
