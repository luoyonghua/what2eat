from pydantic_settings import BaseSettings,SettingsConfigDict



class AuthSettings(BaseSettings):



    jwt_secret:str="your_jwt_secret_key"


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",case_sensitive=False)


auth_settings=AuthSettings()