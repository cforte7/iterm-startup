from dataclasses import dataclass
from typing import Callable, List, Optional

import iterm2


@dataclass
class SessionConfig:
    """A session/subsection within a tab."""

    commands: List[str]  # List of commands to be executed in order.
    purpose: Optional[str]  # Note on the purpose of this session.
    dir: Optional[
        str
    ] = None  # Optional directory to set. If None, it inherits from the TabConfig. Must be full path.
    split_vertical: bool = (
        False  # True will split the tab vertically to create the window.
    )


@dataclass
class TabConfig:
    """A single tab within a window."""

    title: str  # Title of the tab.
    sessions: List[SessionConfig]  # Children Sessions
    dir: str  # Default working directory for all child sessions. Must be full path


def build_iterm_main(configs: List[TabConfig]) -> Callable:
    """Higher order function to create function called by iTerm with provided configs."""

    async def main(connection):
        """Function passed to iTerm to execute opening of the Config objects."""
        await iterm2.async_get_app(connection)  # initialize app
        tab_configs = configs
        window = await iterm2.Window.async_create(connection)
        for config in tab_configs:
            # set tab title from config
            current_tab = await window.async_create_tab()
            await current_tab.async_set_title(config.title)

            # For first time through use session initialized with tab. Rest of time, create new session.
            current_session = None
            for session in config.sessions:
                if current_session is None:
                    current_session = current_tab.current_session
                else:
                    current_session = await current_session.async_split_pane(
                        vertical=session.split_vertical
                    )

                # get dir from session config if present, if not get from tab config
                cwd = session.dir or config.dir
                await current_session.async_send_text(f"cd {cwd}\n")
                for command in session.commands:
                    await current_session.async_send_text(
                        f"{command}\n"  # \n is for carriage return
                    )

        # close out tab the window is initialized with
        await window.tabs[0].async_close()

    return main
