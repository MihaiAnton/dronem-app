import rest_framework.status as rest_status
from rest_framework import permissions as rest_permissions
from rest_framework import viewsets as rest_viewsets
from rest_framework.response import Response

# Create your views here.
from environments.models import Environment
from environments.serializers import EnvironmentSerializer


# TODO: endpoint for adding/deleting a meeting
# TODO: endpoint for adding/deleting a robot

class EnvironmentViewSet(rest_viewsets.ModelViewSet):
    permission_classes = (rest_permissions.IsAuthenticated,)
    serializer_class = EnvironmentSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Environment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=rest_status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for meeting in instance.meetings.all():
            meeting.delete()
        for robot in instance.robots.all():
            robot.delete()
        return super().destroy(request, *args, **kwargs)
