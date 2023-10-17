from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    """
    Telegram bot configuration class.
    This class holds the settings for the token

    Attributes
    ----------
    token : str
        The token received from BotFather.
    group: str
        The unique id in private group
    """
    token: str
    group: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates a Telegram bot configuration object.

        :param env: An Env object containing environment settings.
        :return: A Telegram bot configuration object.
        """
        token = env.str("BOT_TOKEN")
        group = env.str("GROUP")
        return TgBot(token=token, group=group)


@dataclass
class Config:
    """
    Config configuration class
    This class holds the settings for config.

    Attributes
    ----------
    tg_bot: TgBot
        The Telegram bot configuration object
    """
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    """
    Loads the application configuration from an environment file and creates a Config object.

    :param path: Path to the environment file (default is None).
    :return: A config configuration object.
    """
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot.from_env(env))
