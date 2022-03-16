# this only works on Linux
# adjust the path for binarycreator
# change version number for executable in this file
# change the version in config/config.xml
# change the ReleaseDate in packages/.../meta/package.xml 
# should only be called from outside of the source directory


if [ ! -d "ebookcreator" ] 
then
    echo "Directory ebookcreator DOES NOT exists." 
    echo "Make sure you are running this script from one directory above ebookcreator"
    exit 9999
fi

# build executable
if [ -d "build_ebc" ] 
then
    rm -r build_ebc/*
else
    mkdir build_ebc
fi
if [ -d "work_ebc" ] 
then
    rm -r work_ebc/*
else
    mkdir work_ebc
fi

pyinstaller --workpath ./work_ebc --distpath ./build_ebc ./ebookcreator/main.py

#mv packages/com.vendor.product/data/bin/main packages/com.vendor.product/data/bin/EbookCreator

# installer part
if [ -d "installer_ebc" ] 
then
    rm -r installer_ebc/*
else
    mkdir installer_ebc
fi

mkdir installer_ebc/packages
mkdir installer_ebc/packages/at.crowdware.ebc
mkdir installer_ebc/packages/at.crowdware.ebc/meta
mkdir installer_ebc/packages/at.crowdware.ebc/data
mkdir installer_ebc/packages/at.crowdware.ebc/data/bin
mkdir installer_ebc/packages/at.crowdware.ebc/data/themes
mkdir installer_ebc/packages/at.crowdware.ebc/data/sources
mkdir installer_ebc/packages/at.crowdware.ebc/data/books
cp -r build_ebc/main/* installer_ebc/packages/at.crowdware.ebc/data/bin
cp -r ebookcreator/themes/* installer_ebc/packages/at.crowdware.ebc/data/themes
cp ebookcreator/run installer_ebc/packages/at.crowdware.ebc/data
cp ebookcreator/INSTALLER/installscript.qs installer_ebc/packages/at.crowdware.ebc/meta
cp ebookcreator/INSTALLER/package.xml installer_ebc/packages/at.crowdware.ebc/meta
/home/art/Qt/Tools/QtInstallerFramework/4.2/bin/binarycreator -f -c ./ebookcreator/INSTALLER/config.xml -p installer_ebc/packages EbookCreator-Linux-1.3.2.Setup


# Debian part
if [ -d "debian_ebc" ] 
then
    rm -r debian_ebc/*
else
    mkdir debian_ebc
fi
mkdir debian_ebc/DEBIAN
mkdir debian_ebc/usr
mkdir debian_ebc/usr/bin
mkdir debian_ebc/usr/share
mkdir debian_ebc/usr/share/applications
mkdir debian_ebc/usr/share/pixmaps
mkdir debian_ebc/usr/share/ebookcreator
mkdir debian_ebc/usr/share/ebookcreator/bin
mkdir debian_ebc/usr/share/ebookcreator/themes
mkdir debian_ebc/usr/share/ebookcreator/sources
mkdir debian_ebc/usr/share/ebookcreator/books
cp -r ebookcreator/DEBIAN/* debian_ebc/DEBIAN
cp -r build_ebc/main/* debian_ebc/usr/share/ebookcreator/bin
cp -r ebookcreator/themes/* debian_ebc/usr/share/ebookcreator/themes
cp ebookcreator/images/logo.png debian_ebc/usr/share/pixmaps
cp ebookcreator/usr/share/applications/* debian_ebc/usr/share/applications
dpkg -b ./debian_ebc ebookcreator.deb