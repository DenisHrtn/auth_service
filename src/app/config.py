from pydantic import BaseModel, BaseSettings


class DBConfig(BaseModel):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    schema_name: str


class RedisConfig(BaseModel):
    host: str
    port: int


class Config(BaseSettings):
    class Config:
        env_file = ".env"

    DB_CONFIG: DBConfig
    REDIS_CONFIG: RedisConfig
