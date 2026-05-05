from django.contrib import admin
from django.urls import path, include
from app_run.views import company_details, UserViewSet, RunStartApiView, RunStopApiView
from rest_framework.routers import DefaultRouter
from app_run.views import RunViewSet

router = DefaultRouter()
router.register('api/runs', RunViewSet)
router.register('api/users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/company_details/', company_details),
    path('api/runs/<int:run_id>/start/', RunStartApiView.as_view()),
    path('api/runs/<int:run_id>/stop/', RunStopApiView.as_view()),
    path('', include(router.urls)),
    ]


