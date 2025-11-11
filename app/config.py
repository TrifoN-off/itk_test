from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    app_name: str = 'ITK Wallet Service'
    secret_key: str = 'DEV_KEY_CHANGE_IN_PROD'
    debug: bool = True
    database_url: str = (
        'postgresql+asyncpg://dev_user:dev_password@localhost:5432/wallet_db'
    )
    database_echo: bool = True


settings = Settings()
