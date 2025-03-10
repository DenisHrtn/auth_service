import redis
from dependency_injector import containers, providers

from app.application.interactors.confirm_register.confirm_register_interactor import (
    ConfirmRegistrationInteractor,
)
from app.application.interactors.login_interactor import LoginInteractor
from app.application.interactors.register.register_user_interactor import (
    RegisterUserInteractor,
)
from app.application.interactors.send_code_again.send_code_again_intreractor import (
    SendCodeAgainInteractor,
)
from app.config import Config
from app.infra.repos.sqla.db import Database
from app.infra.repos.users.user_repo_impl import UserRepoImpl
from app.infra.services.celery_email_sender import CeleryEmailSender
from app.infra.services.confirm_code import ConfirmCodeService
from app.infra.services.password_hasher import PasswordHasher
from app.infra.unit_of_work.async_sql import UnitOfWork


class DBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)
    db = providers.Singleton(Database, config=config.provided.DB_CONFIG)
    uow = providers.Factory(UnitOfWork, session_factory=db.provided.session_factory)


class RedisContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)

    redis_client = providers.Singleton(
        redis.Redis,
        host=config.provided.REDIS_CONFIG.host,
        port=config.provided.REDIS_CONFIG.port,
        decode_responses=True,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)

    db = providers.Container(DBContainer, config=config)
    redis = providers.Container(RedisContainer, config=config)

    code_service = providers.Singleton(ConfirmCodeService)

    password_hasher = providers.Singleton(PasswordHasher)

    email_sender = providers.Singleton(CeleryEmailSender)

    user_repo = providers.Singleton(UserRepoImpl, uow=db.uow)

    register_user_interactor = providers.Factory(
        RegisterUserInteractor,
        uow=db.uow,
        email_sender=email_sender,
        password_hasher=password_hasher,
        user_repo=user_repo,
    )

    confirm_registration_interactor = providers.Factory(
        ConfirmRegistrationInteractor,
        uow=db.uow,
        code_service=code_service,
        user_repo=user_repo,
    )

    send_code_again_interactor = providers.Factory(
        SendCodeAgainInteractor,
        uow=db.uow,
        email_sender=email_sender,
        code_service=code_service,
        user_repo=user_repo,
    )

    login_interactor = providers.Factory(
        LoginInteractor, uow=db.uow, user_repo=user_repo
    )


container = Container()
