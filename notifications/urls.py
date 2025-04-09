from django.urls import path
from .views import DashboardOverviewView
from .views import AllNotificationsView, MarkNotificationReadView

urlpatterns = [
    path('', AllNotificationsView.as_view(), name='notifications-feed'), 
    path('all/', AllNotificationsView.as_view(), name='all-notifications'),
    path('<int:notification_id>/mark-read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
]
