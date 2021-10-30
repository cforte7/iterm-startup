from .base_models import TabConfig, SessionConfig

CLARITY_DIR = "~/Dev/clarity/"
clarity = TabConfig(
    title="clarity",
    dir=CLARITY_DIR,
    sessions=[
        SessionConfig(
            purpose="Run node server for Clarity React app.", commands=["npm start"]
        ),
        SessionConfig(purpose="Run node server for Clarity React app.", commands=["glo5"]),
    ],
)

TIMBER_DIR = "~/Dev/timbersaw/"
timbersaw = TabConfig(
    title="timbersaw",
    dir=TIMBER_DIR,
    sessions=[
        SessionConfig(purpose="Run FASTAPI server.", commands=["make run-dev"]),
        SessionConfig(purpose="General command line stuff.", commands=["glo5"]),
    ],
)

project_configs = [clarity, timbersaw]
