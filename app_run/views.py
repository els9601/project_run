from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

from .serializers import RunSerializer, UserSerializer
from .models import Run


@api_view(['GET'])
def company_details(request):
    details = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(details)


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete')
    serializer_class = RunSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['last_name', 'first_name']

    def get_queryset(self):
        qs = super().get_queryset()
        user_type = self.request.query_params.get('type')
        if user_type == 'coach':
            return qs.filter(is_staff=True)
        elif user_type == 'athlete':
            return qs.filter(is_staff=False)
        return qs


class RunStartApiView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, pk=run_id)
        if run.status != 'init':
            return Response(
                {"error": "Run cannot be started"},
                status=status.HTTP_400_BAD_REQUEST
            )
        run.status = 'in_progress'
        run.save()
        return Response({
            "id": run.pk,
            "status": run.status
        })


class RunStopApiView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, pk=run_id)
        if run.status != 'in_progress':
            return Response(
                {"error": "Run cannot be stopped"},
                status=status.HTTP_400_BAD_REQUEST
            )
        run.status = 'finished'
        run.save()
        return Response({
            "id": run.pk,
            "status": run.status
        })