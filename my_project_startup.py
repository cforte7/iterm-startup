import iterm2
from configs.base_models import build_iterm_main
from configs.project_configs import project_configs

iterm2.run_until_complete(build_iterm_main(project_configs))
