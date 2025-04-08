from django.urls import path
from .views import DashboardOverviewView
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/mark-read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
]
