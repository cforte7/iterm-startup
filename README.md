# iTerm Startup Automation Templating

This repo is for providing a simple way to automate startup commands in iTerm2 for your different projects. 

# Creating a New Automation

To create a new automation you will need two types of files:
1. Config File
2. Automation Executor


## Setup
First you will need to clone this repo and add the `configs` folder to the iTerm2 Scripts folder, 
found at `~/Library/Application Support/iTerm2/Scripts`.
This directory contains the models that are used to build your custom configurations
and the function to create those configs.

## Config File

You will first need a set of config objects.

The configs are made up of two different dataclasses:

### TabConfig
```python
@dataclass
class TabConfig:
    """A single tab within a window."""
    title: str # title that is given to the tab.
    sessions: List[SessionConfig] # Children Sessions (subsections of tab)
    dir: str # default directory to set each session to 
```

### SessionConfig
```python
@dataclass
class SessionConfig:
    """Represents a session (subdivision) within a tab."""
    cmds: List[str]  # List of commands to be executed upon creation
    split_vertical: bool = False  # True will split the tab vertically to create the window
    dir: Optional[str]
```


### Example Config Objects
```python
from .base_models import TabConfig, SessionConfig #  inside the configs directory

CLARITY_DIR = '~/Dev/clarity/'
clarity = TabConfig(
    title="clarity",
    dir=CLARITY_DIR,
    sessions=[
        SessionConfig(
            cmds=["npm start"]
        ),
        SessionConfig(
            cmds=["git log"]
        )
    ]
)

project_configs = [clarity]  # if you have additional TabConfig objects, add them to this list
```
 
With the above config, we will create a tab that has the title `clarity` and has two sessions.  
The two different sessions will open up stacked vertically with the first running `npm start` and the second running `git log`.

Both will open to the directory `~/Dev/clarity/` as defined on the `TabConfig` class.
If you wanted the session to open up with a different directory all you have to do is specify
`dir=OTHER_PATH` on the `SessionConfig`.


Finally we have:
```
project_configs = [clarity]
``` 
This is a collection of `TabConfig` objects that will be imported into our execution script (explained below).

## Execution Script
Create a new python file in the iTerm `Scripts` folder that can be easily identified as this 
is what you will be selecting when running the automation.

Import `iterm2` along with `from configs.base_models import build_iterm_main` and your project config list if it is 
in another file.

```python
import iterm2
from configs.my_project import project_configs  # file with the config objects
from configs.base_models import build_iterm_main

iterm2.run_until_complete(build_iterm_main(project_configs))
```


Replace `project_configs` in 
```python
iterm2.run_until_complete(build_iterm_main(project_configs))
```
with your array of Config objects and you are all set!

## Running The Script
Open iTerm2 and in your toolbar select Scripts and select the name of your execution script to run it.