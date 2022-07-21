from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    PASSWORD: str = 'password'

    CLUSTER_USER: str = 'dsri_user'
    CLUSTER_PASSWORD: str = 'password'
    CLUSTER_URL: str = 'https://api.dsri2.unimaas.nl:6443'

    SQL_URL: str


    @validator('SQL_URL', pre=True)
    def gen_sql_url(cls, v, values):
        return f"mysql://dsri-user:{values.get('PASSWORD')}@mysql:3306/dsri-db"

    class Config:
        case_sensitive = True


settings = Settings()

