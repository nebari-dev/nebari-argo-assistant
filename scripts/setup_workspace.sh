# One-time Setup of the Nebari workspace
# This script downloads and installs Argo. It also adds helpful items to .bash_profile.

# Setup Argo CLI
# The CLI will allow us to test Argo from the command line and is also used by Hera workflow management

cd ~

# Download the binary. Get the url from the latest release page https://github.com/argoproj/argo-workflows/releases
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.4.8/argo-linux-amd64.gz

# Unzip
gunzip argo-linux-amd64.gz

# Make binary executable
chmod +x argo-linux-amd64

# Create argo directory
mkdir -p ~/bin/argo

# Move binary to path
mv ./argo-linux-amd64 ~/bin/argo

# Add alias to profile
echo "" >> ~/.bash_profile
echo "export PATH=\"$HOME/bin/argo:\$PATH\"" >> ~/.bash_profile
echo "alias argo=\"argo-linux-amd64\"" >> ~/.bash_profile
echo "source ~/.bashrc" >> ~/.bash_profile

# Test installation
argo version

# Other setup
# add local bin to path for pip installed packages
echo "export PATH=\"$HOME/.local/bin:\$PATH\"" >> ~/.bash_profile
