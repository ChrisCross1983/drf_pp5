from django.urls import path
from .views import DashboardOverviewView
from .views import AllNotificationsView, MarkNotificationReadView, MarkAllNotificationsReadView

urlpatterns = [
    path('', AllNotificationsView.as_view(), name='notifications-feed'), 
    path('all/', AllNotificationsView.as_view(), name='all-notifications'),
    path('<int:notification_id>/mark-read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path("mark-all-read/", MarkAllNotificationsReadView.as_view(), name="notifications-mark-all-read"),
    path('overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
]
