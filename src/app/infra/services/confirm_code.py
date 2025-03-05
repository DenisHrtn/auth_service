from app.application.interfaces.confirm_code.confirm_code import IConfirmCode
from app.infra.utils.generate_confirm_code import gen_code


class ConfirmCodeService(IConfirmCode):
    def confirm_code(self) -> int:
        return gen_code()
