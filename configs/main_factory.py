from typing import List
from configs.base_models import TabConfig

import iterm2


def build_iterm_main(configs: List[TabConfig]):
    async def main(connection):
        tab_configs = configs
        window = await iterm2.Window.async_create(connection)
        current_tab = None
        for config in tab_configs:
            current_session = None
            if current_tab is None:
                current_tab = window.current_tab
            else:
                current_tab = await window.async_create_tab()
            await current_tab.async_set_title(config.title)
            for session in config.sessions:
                if current_session is None:
                    current_session = current_tab.current_session
                else:
                    current_session = await current_session.async_split_pane(vertical=session.split_vertical)

                # get dir from session if present, if not get from config
                await current_session.async_send_text(f"cd {config.dir}\n")
                for cmd in session.cmds:
                    await current_session.async_send_text(f"{cmd}\n")
