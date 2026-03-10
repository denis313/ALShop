from dataclasses import dataclass
import environs


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = environs.Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))


def db_config(path: str | None = None) -> str:
    env = environs.Env()
    env.read_env(path)
    url = env('DATABASE_URL')
    return url


def provider_token(path: str | None = None) -> str:
    env = environs.Env()
    env.read_env(path)
    token = env('provider_token')
    return token

def yookassa(path: str | None = None) -> tuple:
    env = environs.Env()
    env.read_env(path)
    account_id = env('account_id')
    secret_key = env('secret_key')
    return account_id, secret_key