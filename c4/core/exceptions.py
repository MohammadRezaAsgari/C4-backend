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

class C4GroupExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "قبلا هسته تشکیل داده اید"

class Core1NotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "کاربر هسته اول وجود ندارد"

class Core2NotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "کاربر هسته دوم وجود ندارد"

class Core3NotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "کاربر هسته سوم وجود ندارد"

class Core1ExistsException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "کاربر هسته اول گروه دارد"

class Core2ExistsException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "کاربر هسته دوم گروه دارد"

class Core3ExistsException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "کاربر هسته سوم گروه دارد"

class C4GroupDoesNotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "هیچ هسته ای برای شما وجود ندارد"
