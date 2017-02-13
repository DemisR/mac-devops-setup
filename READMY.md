# My Mac OS DevOps environment

## Installation

- Install Ansible
- Ensure Apple's command line tools are installed
- Clone this repository to your local drive
- Updating OSX
- Installing Xcode Command Line Tools
- Run `ansible-playbook setup-my-mac.yml -i inventory -K` inside this directory. Enter your account password when prompted.

All commands are listed in [install.sh](install.sh)

    Note: If some Homebrew commands fail, you might need to agree to XCode's license or fix some other Brew issue. Run brew doctor to see if this is the case.

## Terminal setup
- zsh
- zsh-completions
- oh-my-zsh
- iterm2
    - Solarized Dark theme
    - font-inconsolata

## Utilities
- python
- pip
- virtualenv
- virtualenvwrapper
- python3

- ssh-copy-id
- git
- tree
- wget
- homebrew
- mas-cli
- unarchiver
- nmap
- httpie
- csshx
- whatmask (ipcalculator)
- caffeine
- vim
- java
- lanscan



### Install developer friendly quick look plugins; see https://github.com/sindresorhus/quick-look-plugins
brew cask install
  - qlcolorcode
  - qlstephen
  - qlmarkdown
  - quicklook-json
  - qlprettypatch
  - quicklook-csv
  - betterzipql
  - qlimagesize
  - webpquicklook
  - suspicious-package

## Softwares

- 1Password
- ansible
- docker
- kinematic
- vagrant
- virtualbox
- intellij-idea
    - config
- sourcetree
- postman
- dropbox
- google-chrome
    - Bookmarks
    - ublock
    - json viewer
    - xmlviewer
    - save to pocket
    - evernote
    - 1Password
    - Xpath helper


- firefox dev
- slack
- atom
    - Install shell command
    - Packages:
        - atom-beautify
        - block-comment
        - file-icons
        - git-history
        - git-log
        - git-projects
        - git-control
        - language-generic-config
        - language-nagios
        - merge-conflicts
        - open-recent
        - markdown-writer
        - pigments
        - project-manager
        - qulor
- spotify
- outlook
- ms-office
- MicrosofrRemoteDesktop
- evernote
- postico
- sequelpro
- skitch
- skype4b
- vlc


### Optionals
- Dbeaver
- Filezilla
- coconut battery
- archi
- etcher
- gitbook editor
- iStumbler
- Integrity
- LICEcap
- macdown
- MySQLWorkbentch
- SerialTools
- Spark (mail)
- teamviewer
- transmission
- wireshark
- visualvm
- pandoc
- colordiff
- htop
- rsync
- HandBrake
- jmeter


## MacOS settings
### Show icons for hard drives, servers, and removable media on the desktop
defaults write com.apple.finder ShowExternalHardDrivesOnDesktop -bool true
defaults write com.apple.finder ShowMountedServersOnDesktop -bool true
defaults write com.apple.finder ShowRemovableMediaOnDesktop -bool true
### Avoid creating .DS_Store files on network volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true

## Personal soft and setup
- PWmanager scripts

### VPN setup

### GIT global config

### Mail setup

### Dotfiles




## Testing the Playbook
Use Mac virtualbox https://github.com/geerlingguy/macos-virtualbox-vm

## Links
https://blog.vandenbrand.org/2016/01/04/how-to-automate-your-mac-os-x-setup-with-ansible/
http://www.nickhammond.com/automating-development-environment-ansible/
https://github.com/simplycycling/ansible-mac-dev-setup/blob/master/main.yml
https://github.com/mas-cli/mas
https://github.com/geerlingguy/mac-dev-playbook
https://github.com/osxc
https://github.com/MWGriffin/ansible-playbooks/blob/master/sourcetree/sourcetree.yaml   
