# Install JATIC related tools into the current environment. This
# will install the shared repo directories into your local user space.

# Setting ROOT in this way installs from the shared folder.
# If you'd like to install using your own copy of these tools, run
# `./install_jatic_tools.sh` and change the ROOT to point to that directory.

ROOT=$HOME/jatic/git

JATIC_TOOLBOX=$ROOT/jatic-toolbox/
ARMORY=$ROOT/armory/
PLATFORM_WORKFLOWS=$ROOT/platform-workflows/
XAITC_CDAO=$ROOT/xaitk-cdao/
XAITC_SALIENCY=$ROOT/xaitk-saliency/


pip install $JATIC_TOOLBOX
pip install $ARMORY
pip install $PLATFORM_WORKFLOWS
pip install $XAITC_CDAO
pip install $XAITC_SALIENCY
