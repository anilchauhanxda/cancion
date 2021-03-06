
import asyncio
import importlib.util
import logging
from pathlib import Path

from telethon import TelegramClient
import telethon.utils
import telethon.events

from . import hacks

TG_BOT_TOKEN_BF_HER = None
TG_BOT_USER_NAME_BF_HER = None 

class meanii(TelegramClient):
    def __init__(
            self, session, *, n_plugin_path="plugins", db_plugin_path="plugins",
            bot_token=None, api_config=None, **kwargs):
        self._name = "LoggedIn"
        self._logger = logging.getLogger("meanii")
        self._plugins = {}
        self.n_plugin_path = n_plugin_path
        self.db_plugin_path = db_plugin_path
        self.config = api_config

        kwargs = {
            "api_id": 6,
            "api_hash": "eb06d4abfb49dc3eeb1aeb98ae0f581e",
            "device_model": "GNU/Linux nonUI",
            "app_version": "@meanii 2.0",
            "lang_code": "ml",
            **kwargs
        }

        self.tgbot = None
        if TG_BOT_USER_NAME_BF_HER is not None:
            # ForTheGreatrerGood of beautification
            self.tgbot = TelegramClient(
                "TG_BOT_TOKEN",
                api_id=api_config.APP_ID,
                api_hash=api_config.API_HASH
            ).start(bot_token=TG_BOT_TOKEN_BF_HER)

        super().__init__(session, **kwargs)

        # This is a hack, please avert your eyes
        # We want this in order for the most recently added handler to take
        # precedence
        self._event_builders = hacks.ReverseList()

        self.loop.run_until_complete(self._async_init(bot_token=bot_token))

        core_plugin = Path(__file__).parent / "_core.py"
        self.load_plugin_from_file(core_plugin)

        inline_bot_plugin = Path(__file__).parent / "_inline_bot.py"
        self.load_plugin_from_file(inline_bot_plugin)

        for a_plugin_path in Path().glob(f"{self.n_plugin_path}/*.py"):
            self.load_plugin_from_file(a_plugin_path)

        
    async def _async_init(self, **kwargs):
        await self.start(**kwargs)

        self.me = await self.get_me()
        self.uid = telethon.utils.get_peer_id(self.me)

        self._logger.info(f"Logged in as {self.uid}")


    def load_plugin(self, shortname):
        self.load_plugin_from_file(f"{self.n_plugin_path}/{shortname}.py")

    def load_plugin_from_file(self, path):
        path = Path(path)
        shortname = path.stem
        name = f"_meaniiPlugins.{self._name}.{shortname}"

        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)

        mod.songsxd = self
        mod.logger = logging.getLogger(shortname)
        # declare Config and tgbot to be accessible by all modules
        mod.Config = self.config
        if TG_BOT_USER_NAME_BF_HER is not None:
            mod.tgbot = self.tgbot


        spec.loader.exec_module(mod)
        self._plugins[shortname] = mod
        self._logger.info(f"Successfully loaded plugin {shortname}")

    def remove_plugin(self, shortname):
        name = self._plugins[shortname].__name__

        for i in reversed(range(len(self._event_builders))):
            ev, cb = self._event_builders[i]
            if cb.__module__ == name:
                del self._event_builders[i]

        del self._plugins[shortname]
        self._logger.info(f"Removed plugin {shortname}")

    def await_event(self, event_matcher, filter=None):
        fut = asyncio.Future()

        @self.on(event_matcher)
        async def cb(event):
            try:
                if filter is None or await filter(event):
                    fut.set_result(event)
            except telethon.events.StopPropagation:
                fut.set_result(event)
                raise

        fut.add_done_callback(
            lambda _: self.remove_event_handler(cb, event_matcher))

        return fut
