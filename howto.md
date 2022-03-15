# How To

## Create Debian Package
cd /home/[user]/SourceCode
dpkg -b ./ebookcreator ebookcreator.deb

## Deinstall Debian Package
sudo apt-get remove ebookcreator

## Install Debian Package
sudo dpkg -i ebookcreator.deb