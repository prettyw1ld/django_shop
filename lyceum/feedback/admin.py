__all__ = []

import django.contrib.admin
import feedback.models


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
    )
    list_display_links = (feedback.models.Feedback.name.field.name,)
