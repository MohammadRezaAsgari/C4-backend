from rest_framework.exceptions import APIException
from rest_framework import status


class UserExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "کاربر از قبل وجود دارد"

class PhoneIsUsedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "شماره تلفن از قبل استفاده شده است"

class UserNotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "کاربر وجود ندارد"

class PassIncorrectException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "کد اشتباه است"