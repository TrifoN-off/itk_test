from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    app_name: str = 'ITK Wallet Service'
    secret_key: str = 'DEV_KEY_CHANGE_IN_PROD'
    debug: bool = True
    database_echo: bool = True

    postgres_user: str = 'dev_user'
    postgres_password: str = 'dev_password'
    postgres_host: str = 'db'
    postgres_port: int = 5432
    postgres_db: str = 'mydatabase'

    @property
    def database_url(self) -> str:
        user_pass = f'{self.postgres_user}:{self.postgres_password}'
        host_port = f'{self.postgres_host}:{self.postgres_port}'
        db_name = self.postgres_db

        return f'postgresql+asyncpg://{user_pass}@{host_port}/{db_name}'


settings = Settings()
