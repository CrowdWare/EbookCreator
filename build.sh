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
cp ebookcreator/DEBIAN/changelog debian_ebc/DEBIAN
cp ebookcreator/DEBIAN/control debian_ebc/DEBIAN
cp ebookcreator/DEBIAN/copyright debian_ebc/DEBIAN
cp ebookcreator/DEBIAN/ebookcreator.desktop debian_ebc/usr/share/applications
cp -r build_ebc/main/* debian_ebc/usr/share/ebookcreator/bin
cp -r ebookcreator/themes/* debian_ebc/usr/share/ebookcreator/themes
cp ebookcreator/images/logo.png debian_ebc/usr/share/pixmaps

dpkg -b ./debian_ebc ebookcreator.deb