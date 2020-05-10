import threading

import rest_framework.generics as rest_generics
import rest_framework.permissions as rest_perimssions
import rest_framework.status as rest_status
from celery.task import task
from celery.utils.log import get_task_logger
from rest_framework.response import Response

from environments.models import Environment
from rl.q_learning import QLearning
from rl.serializers import TrainSerializer

logger = get_task_logger(__name__)


@task(name="train_celery_task")
def train_task(env_name: str) -> None:
    logger.info("Train Task started")
    dronem_env = Environment.objects.get(name=env_name).to_gym_env
    q_learning = QLearning(dronem_env)
    q_learning.train()


class MyThread(threading.Thread):

    def __init__(self, env):
        threading.Thread.__init__(self)
        self.__env = env

    def run(self):
        q_learning = QLearning(self.__env)
        q_learning.train()


class TrainView(rest_generics.CreateAPIView):
    serializer_class = TrainSerializer
    permission_classes = (rest_perimssions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        env_name = serializer.validated_data.get('env_name')
        dronem_env = Environment.objects.get(name=env_name).to_gym_env
        train_task.delay(env_name)
        # # MyThread(dronem_env).start()
        # q_learning = QLearning(dronem_env)
        # q_learning.train()
        return Response(status=rest_status.HTTP_201_CREATED, data=dronem_env.get_env_metadata())
