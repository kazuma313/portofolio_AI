from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_option: list = [
        "Natural Language Processing",
        "Computer Vision",
        "Data Science",
        "Certificate",
        "Curriculum Vitae",
    ]
    model_config = SettingsConfigDict(env_prefix="my_prefix_")


if __name__ == "__main__":
    print(Settings().project_option)
    print(Settings().model_dump())
