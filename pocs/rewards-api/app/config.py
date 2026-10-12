from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["resources/settings.toml", "resources/.secrets.toml"],
    environments=True,
    env_switcher="APP_ENV",
)
