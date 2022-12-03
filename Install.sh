#!/bin/bash

printf "# Step 1 : Installing Xcode Command Line Tools"
xcode-select --install

echo "# Step 2 : Installing Homebrew"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew doctor

echo "# Step 3 : Installing Python3"
brew install python
echo 'export PATH="/usr/local/opt/python/libexec/bin:$PATH"' >> ~/.zshrc
export PATH="/usr/local/opt/python/libexec/bin:$PATH"

# Install PIP
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# sudo python get-pip.py

echo "# Step 4 : Installing Ansible"
sudo pip install ansible

echo "# Step 5 : Installing Git"
brew install git

echo "# Step 6 : Installing Ansible dependency collections"
ansible-galaxy install -r requirements.yml

while true; do
    read -p "Would you like execute the playbook now? (y/n) " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) printf "\n Execute this command when you are ready:\n  ansible-playbook setup-my-mac.yml -i inventory -K \n" ; exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "# Running ansible setup"
ansible-playbook setup-my-mac.yml -i inventory -K