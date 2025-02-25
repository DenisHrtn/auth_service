from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    schema_name: str

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "allow"


# class RedisConfig(BaseSettings):
#     redis_host: str
#     redis_port: int
#
#     class Config:
#         env_file = ".env"
#         env_nested_delimiter = "__"
#         extra = "allow"


class Config(BaseSettings):
    DB_CONFIG: DBConfig
    # REDIS_CONFIG: RedisConfig

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "allow"
