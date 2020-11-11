from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.core.signals import request_finished

from notifications import models


class NotificationsView(LoginRequiredMixin, ListView):
    model = models.Notification
    template_name = 'pages/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 100

    # def get(self, request, *args, **kwargs):
    #     response = super().get(request, *args, **kwargs)
    #     unread_notifications = self.model.objects.filter(user__id=request.user.id, read=False)
    #     if unread_notifications.exists():
    #         unread_notifications.update(read=True)
    #     return response

    def get_queryset(self):
        return self.model.objects.filter(
            user__id=self.request.user.id
        )


@require_POST
@login_required
def get_notifications(request, **kwargs):
    notifications = models.Notification.objects\
                    .filter(user__id=request.user.id, read=False)
    return JsonResponse(data={
        'total': notifications.count(),
        'notifications': notifications
    })
