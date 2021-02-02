# Installing Xcode Command Line Tools
xcode-select --install

# install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew doctor

# Install python3
brew install python
echo 'export PATH="/usr/local/opt/python/libexec/bin:$PATH"' >> ~/.zshrc
export PATH="/usr/local/opt/python/libexec/bin:$PATH"

# Install PIP
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# sudo python get-pip.py

# Install Ansible
sudo pip install ansible
brew install git

# Clone this repository to your local drive
git clone https://github.com/DemisR/mac-devops-setup.git

# Updating OSX

# Run `ansible-playbook setup-my-mac.yml -i inventory -K` inside this directory. Enter your account password when prompted.
cd mac-devops-setup
ansible-galaxy collection install community.general

ansible-playbook setup-my-mac.yml -i inventory -K
