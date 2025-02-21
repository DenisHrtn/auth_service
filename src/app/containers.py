import redis.asyncio as redis
from dependency_injector import containers, providers

from src.app.config import Config
from src.app.infra.repos.sqla.db import Database
from src.app.infra.unit_of_work.async_sql import UnitOfWork


class DBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)
    db = providers.Singleton(Database, config=config.provided.DBConfig)
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
    config = Config()

    db = providers.Container(DBContainer, config=config)
    redis = providers.Container(RedisContainer, config=config)
