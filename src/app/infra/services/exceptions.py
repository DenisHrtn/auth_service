class EmailServiceBaseException(Exception):
    pass


class SendMessageError(EmailServiceBaseException):
    pass
