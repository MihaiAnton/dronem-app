"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   29.04.2020 21:34
"""
import rest_framework.status as rest_status
from rest_framework.exceptions import APIException


class InvalidRobotIdError(APIException):
    status_code = rest_status.HTTP_400_BAD_REQUEST
    default_code = 'robot_id_not_found'
    default_detail = 'invalid robot id'


class EnvironmentIncompleteError(APIException):
    status_code = rest_status.HTTP_400_BAD_REQUEST
    default_code = 'environment_is_incomplete'
    default_detail = 'environment incomplete'
