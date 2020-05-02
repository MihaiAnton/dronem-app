from django.db import models
from django_mysql.models import ListTextField

from environments.env_interpretation import MeetingEnv
from environments.envs import DronemEnv
from environments.exceptions import EnvironmentIncompleteError


class Environment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    num_robots = models.IntegerField()
    max_memory = models.IntegerField()
    init_memory = models.IntegerField()
    collect_memory = models.IntegerField(null=True)

    @property
    def cycles(self):
        cycle_lst = []
        for r in self.robots.all():
            cycle_lst.append(r.cycle)
        return cycle_lst

    @property
    def to_gym_env(self) -> DronemEnv:
        """
        Property to convert a model Environment to a DronemEnvironment
        :return: DronemEnv
        """
        if not self.robots.all() or not self.meetings.all():
            raise EnvironmentIncompleteError
        meetings = [MeetingEnv(r1=meeting.robot1.r_id, r2=meeting.robot2.r_id, first_time=meeting.first_time)
                    for meeting in self.meetings.all()]
        robots = self.robots.all()
        robots = sorted(list(robots), key=lambda x: x.r_id)
        cycles = [robot.cycle for robot in robots]
        return DronemEnv(
            num_robots=self.num_robots,
            max_memory=self.max_memory,
            init_memory=self.init_memory,
            meetings=meetings,
            cycles=cycles
        )

    def __str__(self):
        return f"{self.name} - {self.num_robots} - {self.meetings.all()} - {self.robots.all()} - {self.cycles}"


class Robot(models.Model):
    r_id = models.IntegerField()  # internal id
    current_memory = models.IntegerField()
    cycle = ListTextField(
        base_field=models.IntegerField(),
        size=255
    )
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='robots')

    def __str__(self):
        return f"{self.r_id} - {self.current_memory}  - {self.cycle} - {self.environment.name}"


class Meeting(models.Model):
    robot1 = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name='r1_meetings')
    robot2 = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name='r2_meetings')
    first_time = models.IntegerField(default=1)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='meetings')

    def __str__(self):
        return f"{self.robot1}-{self.robot2}-{self.first_time}"
