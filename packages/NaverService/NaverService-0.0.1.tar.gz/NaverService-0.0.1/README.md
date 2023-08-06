
# Naver Services


##### ============================================================
## Overview
##### ============================================================


##### ============================================================
## IDE :: Platform Layer
##### ============================================================

mkdir project_name
mkdir package_name
git init
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

##### ============================================================
## IDE :: Application Layer
##### ============================================================

### Terminal

python ide.py

### Jupyter

import os
import sys
sys.path.append(f"{os.environ['HOME']}/pjts/PROJECT_NAME")
import ide
ide.main(ide='jupyter')
ide.setup_logpath(modulepath='jupyter.MODULE_NAME')
