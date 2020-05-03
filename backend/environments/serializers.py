"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   28.04.2020 20:28
"""

import ast

import rest_framework.serializers as rest_serializers

from environments.exceptions import InvalidRobotIdError
from environments.models import Environment
from environments.models import Meeting
from environments.models import Robot


class RobotSerializer(rest_serializers.ModelSerializer):
    r_id = rest_serializers.IntegerField()

    class Meta:
        model = Robot
        fields = ('r_id', 'current_memory', 'cycle',)

    def validate_r_id(self, value):
        if value < 0:
            raise rest_serializers.ValidationError(
                "Robot internal id cannot be negative"
            )
        return value

    def validaate_current_memory(self, value):
        if value < 0:
            raise rest_serializers.ValidationError(
                "Memory cannot be a negative value"
            )
        return value

    def validate_cycle(self, cycle):
        try:
            cycle = ast.literal_eval(cycle)
        except SyntaxError:
            raise rest_serializers.ValidationError(
                "Cycle node must be an integer"
            )
        if len(set(cycle)) != len(cycle):
            raise rest_serializers.ValidationError(
                "Cycle must contain distinct values"
            )
        return cycle

    def create(self, validated_data):
        env = validated_data.get('environment')
        validated_data['current_memory'] = env.init_memory

        return Robot.objects.create(**validated_data)


class RobotField(rest_serializers.Field):
    def to_representation(self, value):
        if not isinstance(value, int):
            return value.r_id
        return value

    def to_internal_value(self, data):
        return data


class MeetingSerializer(rest_serializers.ModelSerializer):
    robot1 = RobotField()
    robot2 = RobotField()

    class Meta:
        model = Meeting
        fields = ('first_time', 'robot1', 'robot2',)

    def validate_first_time(self, value):
        if value < 0:
            raise rest_serializers.ValidationError(
                "Time cannot be a negative value"
            )
        return value

    def validate(self, attrs):
        r_id1 = attrs['robot1']
        r_id2 = attrs['robot2']

        if r_id1 < 0 or r_id2 < 0:
            raise rest_serializers.ValidationError(
                "Robot id cannot be a negative value"
            )
        if r_id1 == r_id2:
            raise rest_serializers.ValidationError(
                "A robot cannot meet with himself"
            )
        return attrs

    def create(self, validated_data):
        env = validated_data['environment']
        id1 = validated_data['robot1']
        id2 = validated_data['robot2']
        if id1 > id2:
            id1, id2 = id2, id1
        try:
            r1 = Robot.objects.get(environment=env,
                                   r_id=id1)
            r2 = Robot.objects.get(environment=env,
                                   r_id=id2)
        except Robot.DoesNotExist:
            raise InvalidRobotIdError
        return Meeting.objects.create(robot1=r1, robot2=r2,
                                      first_time=validated_data['first_time'],
                                      environment=env)


class EnvironmentSerializer(rest_serializers.ModelSerializer):
    collect_memory = rest_serializers.IntegerField(required=False)
    robots = RobotSerializer(many=True)
    meetings = MeetingSerializer(many=True)
    num_robots = rest_serializers.IntegerField()

    class Meta:
        model = Environment
        fields = ('num_robots', 'name', 'max_memory', 'init_memory', 'robots', 'collect_memory', 'meetings',)

    def create(self, validated_data):
        robots_validated_data = validated_data.pop('robots')
        meetings_validated_data = validated_data.pop('meetings')

        env = Environment.objects.create(**validated_data)
        robots_serializer = self.fields['robots']
        meetings_serializer = self.fields['meetings']

        for robot in robots_validated_data:
            robot['environment'] = env

        for meeting in meetings_validated_data:
            meeting['environment'] = env

        robots_serializer.create(robots_validated_data)
        meetings_serializer.create(meetings_validated_data)

        return env

    def update(self, instance, validated_data):
        """
        # TODO: only let update -> environment properties
        # TODO: only let update -> robot's cycles and current memory
        # TODO: only let update -> meetings first time
        """

        instance.num_robots = validated_data.get('num_robots', instance.num_robots)
        instance.name = validated_data.get('name', instance.name)
        instance.init_memory = validated_data.get('init_memory', instance.init_memory)
        instance.collect_memory = validated_data.get('collect_memory', instance.collect_memory)
        instance.save()

        robots_new_data = validated_data.get('robots')
        for robot_data in robots_new_data:
            r_id = robot_data.get('r_id')

            robot = Robot.objects.get(r_id=r_id, environment=instance)
            robot.cycle = robot_data.get('cycle', robot.cycle)
            robot.current_memory = robot_data.get('current_memory', robot.current_memory)
            robot.save()

        meetings_data = validated_data.get('meetings')
        for meeting_data in meetings_data:
            r1_id = meeting_data.get('robot1')
            r2_id = meeting_data.get('robot2')
            meeting = Meeting.objects.get(robot1__r_id=r1_id, robot2__r_id=r2_id, environment=instance)
            meeting.first_time = meeting_data.get('first_time', meeting.first_time)
            meeting.save()

        return instance
