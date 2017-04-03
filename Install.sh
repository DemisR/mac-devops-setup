
# Install PIP
sudo easy_install pip

# Install Ansible
sudo pip install ansible

# Installing Xcode Command Line Tools
xcode-select --install

# Clone this repository to your local drive
git clone https://github.com/DemisR/mac-devops-setup.git

# Updating OSX

# Run `ansible-playbook setup-my-mac.yml -i inventory -K` inside this directory. Enter your account password when prompted.
cd mac-devops-setup
ansible-playbook setup-my-mac.yml -i inventory -K