import iterm2
from configs.dota_interaction import project_configs
from configs.base_models import build_iterm_main

main = build_iterm_main(project_configs)
iterm2.run_until_complete(main)
