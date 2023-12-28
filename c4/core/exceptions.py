from rest_framework.exceptions import APIException
from rest_framework import status


class ParticipationExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "قبلا در این پروژه شرکت کرده اید"

class ParticipationOwnerException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "شما مالک این عضویت نیستید"

class ParticipationPaymentException(APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = "پرداخت شما تایید نشده است"

class ParticipationDoesNotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "عضویت شما برای پروژه وجود ندارد"

class ProjectIsNotRegisteringException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "این پروژه در مرحله ثبت نام قرار ندارد"
