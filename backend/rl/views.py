import rest_framework.generics as rest_generics
import rest_framework.permissions as rest_perimssions
import rest_framework.status as rest_status
from rest_framework.response import Response

from environments.models import Environment
from rl.q_learning import QLearning
from rl.serializers import TrainSerializer


class TrainView(rest_generics.CreateAPIView):
    serializer_class = TrainSerializer
    permission_classes = (rest_perimssions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        env_name = serializer.validated_data.get('env_name')
        dronem_env = Environment.objects.get(name=env_name).to_gym_env
        q_learning = QLearning(dronem_env)
        # q_learning.train() commented this
        return Response(status=rest_status.HTTP_201_CREATED, data=dronem_env.get_env_metadata())
