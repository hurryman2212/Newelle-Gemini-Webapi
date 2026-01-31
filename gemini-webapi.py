from .extensions import NewelleExtension
from .handlers import HandlerDescription
from .handlers.llm import GeminiHandler
from .utility.pip import find_module, install_module

import asyncio, json, os, re, sys

from gemini_webapi import GeminiClient, set_log_level
from loguru import logger
from typing import Callable, Any

LOG_LEVEL = "TRACE"
set_log_level(LOG_LEVEL)
logger.add(
    sys.stderr,
    level=LOG_LEVEL,
    filter=lambda record: record["extra"].get("class_name") == "GeminiWebapiHandler",
)


class GeminiWebapiExtension(NewelleExtension):
    id = "gemini-webapi"
    name = "Gemini Web API Extension"

    def get_llm_handlers(self) -> list:
        return [
            HandlerDescription(
                "geminiwebapi", "gemini-webapi", "Gemini Web API", GeminiWebapiHandler
            )
        ]


class GeminiWebapiHandler(GeminiHandler):
    key = "geminiwebapi"

    def __init__(self, settings, path):
        super().__init__(settings, path)

        self.logger = logger.bind(class_name="GeminiWebapiHandler")

    def is_installed(self) -> bool:
        return bool(find_module("gemini_webapi")) and bool(
            find_module("browser-cookie3")
        )

    def install(self):
        install_module("gemini_webapi", self.pip_path)
        install_module("browser-cookie3", self.pip_path)

    def generate_text_stream(
        self,
        prompt: str,
        history: list[dict[str, str]] = [],
        system_prompt: list[str] = [],
        on_update: Callable[[str], Any] = lambda _: None,
        extra_args: list = [],
    ) -> str:
        async def _inner(prompt, history, system_prompt):
            self.logger.debug("Starting...")

            client = GeminiClient()
            await client.init(
                timeout=180, auto_close=True, close_delay=300, auto_refresh=True
            )
            self.logger.debug(f"prompt: {prompt}")
            self.logger.debug(f"history: {history}")
            self.logger.debug(f"system_prompt: {system_prompt}")

            uuid_to_search = None
            uuid_to_update = None
            if len(history):
                if len(history) == 2:
                    uuid_to_update = history[1]["UUID"]
                    history.append({"User": history[0]["User"], "Message": prompt})
                    prompt = history
                else:
                    uuid_to_search = str(history[-3]["UUID"])
                    uuid_to_update = str(history[-1]["UUID"])
            self.logger.debug(f"uuid_to_search: {uuid_to_search}")
            self.logger.debug(f"uuid_to_update: {uuid_to_update}")

            FILEPATH_PATTERN = r"```(?:image|file)(?:\\n|\s)+([\s\S]*?)(?:\\n|\s)+```"
            file_paths = []
            # if `prompt` type is list,
            if isinstance(prompt, list):
                for each_dict in prompt:
                    extracted_paths = re.findall(FILEPATH_PATTERN, each_dict["Message"])
                    file_paths += [path.strip() for path in extracted_paths]
            else:
                extracted_paths = re.findall(FILEPATH_PATTERN, prompt)
                file_paths += [path.strip() for path in extracted_paths]
            self.logger.debug(f"file_paths: {file_paths}")

            GEM_NAME = "gemini-webapi"
            self.logger.info(f"Fetching old {GEM_NAME} gem...")
            await client.fetch_gems()
            old_gem = client.gems.get(name=GEM_NAME)
            if old_gem is None:
                self.logger.info(f"No existing gem found: Creating {GEM_NAME} gem...")
                updated_gem = await client.create_gem(
                    name=GEM_NAME,
                    prompt=system_prompt,
                )
            else:
                # self.logger.warning(f"Updating old {GEM_NAME} gem...")
                # updated_gem = await client.update_gem(
                #     gem=old_gem,
                #     name=GEM_NAME,
                #     prompt=system_prompt,
                # )
                self.logger.warning(f"Using existing {GEM_NAME} gem...")
                updated_gem = old_gem

            CACHE_FILEPATH = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "cache.json"
            )
            previous_session = None
            # if cache file does not exist, create an empty one
            if not os.path.exists(CACHE_FILEPATH):
                with open(CACHE_FILEPATH, "w+") as cache_file:
                    json.dump({}, cache_file)
            # Load cache JSON file and search for the metadata binary with `uuid_to_search` as key
            with open(CACHE_FILEPATH, "r") as cache_file:
                try:
                    cache_data = json.load(cache_file)
                except:
                    cache_data = {}
            self.logger.debug(f"cache_data: {cache_data}")
            if uuid_to_search:
                previous_session = cache_data[uuid_to_search]
            self.logger.debug(f"previous_session: {str(previous_session)}")

            chat = client.start_chat(
                model="gemini-3.0-pro",
                gem=updated_gem,
                metadata=previous_session,
            )
            self.logger.info(f"Sending request with {GEM_NAME} gem...")
            resp = await chat.send_message(str(prompt), files=file_paths)

            self.logger.info("Response received: " + str(resp))
            print(resp.text)

            # Save the metadata binary to cache JSON file with `uuid_to_update` as key
            # (if cache file does not exist, create an empty one)
            self.logger.debug(f"uuid_to_update: {uuid_to_update}")
            if uuid_to_update:
                with open(CACHE_FILEPATH, "w+") as cache_file:
                    cache_data[uuid_to_update] = chat.metadata
                    # Delete previous file content before writing
                    cache_file.truncate(0)
                    json.dump(cache_data, cache_file)

            self.logger.debug("Completed.")

            return resp.text

        return asyncio.run(_inner(prompt, history, system_prompt))
