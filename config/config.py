from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_url: str = "https://www.saucedemo.com"
    standard_user: str = "standard_user"
    locked_out_user: str = "locked_out_user"
    problem_user: str = "problem_user"
    performance_glitch_user: str = "performance_glitch_user"
    password: str = "secret_sauce"
    timeout: int = 30_000
    headless: bool = False

    model_config = {"env_prefix": "SAUCE_", "env_file": ".env"}


config = Config()
