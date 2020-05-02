"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   02.05.2020 20:02
"""

import rest_framework.serializers as rest_serializers

from environments.models import Environment


class TrainSerializer(rest_serializers.Serializer):
    """
    TODO Add rest of the training parameters
    """
    env_name = rest_serializers.CharField(max_length=255, required=True)

    def validate_env_name(self, value):
        try:
            env = Environment.objects.get(name=value)
        except Environment.DoesNotExist:
            raise rest_serializers.ValidationError(
                f"Environment with name {value} does not exist"
            )

        return value
