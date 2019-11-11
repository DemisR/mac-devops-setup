# 💻 DevOps Mac OS automated setup 

This ansible playbook install and setup most of softwares and utilities for my DevOps environment.

## 🚥 Installation 

First of all clone or download this repository on you mac.

After that you need to do some things to install prerequisites.

- Install Ansible
- Ensure Apple's command line tools are installed
- Clone this repository to your local drive
- Updating OSX
- Installing Xcode Command Line Tools

More easily, you can simply run the [install.sh](install.sh) script which includes all commands for the installation prerequisites.

_Note: If some Homebrew commands fail, you might need to agree to XCode's license or fix some other Brew issue. Run brew doctor to see if this is the case._

For enabling some options and setup alias etc. I clone my dot files repo ( `.zshrc`,`.aliases`,`.gitignore_global`,...).

Of course you can use yours changing `dotfiles_repo` variable in `default.config.yml` file.

## 🚀 Usage

Just run the following command at the root of this project and enter your account password when prompted.

```sh
ansible-playbook setup-my-mac.yml -i inventory -K
```

You can customize setup editing `default.config.yml` config file.


## ✨What this playbook do

The complete list of softwares installed is in `default.config.yml` , but in summary here what the playbook do.

- Install homebrew and cask and install applications, utilities and quick look plugins. 

    Docker, Vagrant, slack, 1password, postman,...

- Clone my dotfile from github repository.

- Install mas (Mac App Store command line interface)

- Configure terminal

    Install iTerm2 (Solarized Dark theme, font-inconsolata)
    Install Zsh and configure options with oh-my-zsh

- Configure Mac OS 

    Show icons for hard drives, servers, and removable media on the desktop
    Avoid creating .DS_Store files on network volumes
    Finder: show status bar
    Save screenshots in PNG format
    Save screenshots to the Desktop/Screenshots folder

- Install VScode and lot of plugins.

    Ansible, Yaml, Golang, Kubernetes, Terraform,...

## Improvements

Configure iTerm2 Profile with Solarized theme.

Install Goolge Chrome extensions

- Adblock Plus
- 1Password extension
- Grammarly for Chrome
- JSON Viewer
- JWT Analyzer & Inspector
- save to pocket

Configure VPN

## Testing the Playbook

Use Mac virtualbox https://github.com/geerlingguy/macos-virtualbox-vm

## See also

- https://blog.vandenbrand.org/2016/01/04/how-to-automate-your-mac-os-x-setup-with-ansible/
- http://www.nickhammond.com/automating-development-environment-ansible/
- https://github.com/simplycycling/ansible-mac-dev-setup/blob/master/main.yml
- https://github.com/mas-cli/mas
- https://github.com/geerlingguy/mac-dev-playbook
- https://github.com/osxc
- https://github.com/MWGriffin/ansible-playbooks/blob/master/sourcetree/sourcetree.yaml   
- https://github.com/sindresorhus/quick-look-plugins