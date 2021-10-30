# iTerm Startup Automation Templating

This repo is for providing a simple way to automate startup commands in iTerm2 for your different projects. 

# Creating a New Automation

To create a new automation you will need two things:
1. Config File
2. Automation Executor

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


### Example
Below is an example of a TabConfig with two SessionConfig children.
```python
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
```
 
With the above config, we will create a tab that has the title `clarity` and has two sessions.  
The two different sessions will open up stacked vertically with the first running `npm start` and the second running `git log`.
Both will open to the directory `~/Dev/clarity/` as defined on the `TabConfig` class.
If you wanted the session to open up with a different directory all you have to do is specify
`dir=OTHER_PATH` on the `SessionConfig`.



