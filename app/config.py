from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


# class Settings(BaseSettings):
#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASS: str
#     DB_NAME: str
#     DATABASE_URL: str
#
#     @model_validator(mode='before')
#     def get_database_url(cls, v):
#         v['DATABASE_URL'] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
#         return v
#
#     class Config:
#         env_file = ".env"

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Со 2 версии Pydantic, class Config был заменен на атрибут model_config
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()