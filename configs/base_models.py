from dataclasses import dataclass
from typing import Callable, List
import logging
import iterm2

logger = logging.getLogger()

@dataclass
class SessionConfig:
    """Represents a session within a tab."""
    cmds: List[str]  # List of commands to be executed
    purpose: str
    split_vertical: bool = False  # True will split the tab vertically to create the window

@dataclass
class TabConfig:
    """A single tab within a window."""
    title: str
    sessions: List[SessionConfig]
    dir: str


def build_iterm_main(configs: List[TabConfig]) -> Callable:
    async def main(connection):
        # not sure why you need this but you have to get the app.
        await iterm2.async_get_app(connection)
        tab_configs = configs
        window = await iterm2.Window.async_create(connection)
        for config in tab_configs:
            current_session = None
            current_tab = await window.async_create_tab()
            await current_tab.async_set_title(config.title)
            for session in config.sessions:
                if current_session is None:
                    current_session = current_tab.sessions[0]
                else:
                    current_session = await current_session.async_split_pane(vertical=session.split_vertical)

                # get dir from session if present, if not get from config
                await current_session.async_send_text(f"cd {config.dir}\n")
                for cmd in session.cmds:
                    await current_session.async_send_text(f"{cmd}\n")
        await window.tabs[0].async_close()
    return main
