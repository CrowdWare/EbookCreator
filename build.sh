# this only works on Linux
# adjust the path for binarycreator
# change version number for executable in this file
# change the version in config/config.xml
# change the ReleaseDate in packages/.../meta/package.xml 


rm -r dist/*
rm -r packages/com.vendor.product/data/*
pyinstaller main.py
mkdir packages/com.vendor.product/data/bin
mkdir packages/com.vendor.product/data/themes
mkdir packages/com.vendor.product/data/sources
mkdir packages/com.vendor.product/data/books
cp -r dist/main/* packages/com.vendor.product/data/bin
cp -r themes/* packages/com.vendor.product/data/themes
cp AppRun packages/com.vendor.product/data
mv packages/com.vendor.product/data/bin/main packages/com.vendor.product/data/bin/EbookCreator
/home/art/Qt/Tools/QtInstallerFramework/3.1/bin/binarycreator -f -c config/config.xml -p packages EbookCreator-Linux-1.3.2.Setup


# Debian part
rm -r usr/share/ebookcreator/bin/*
rm -r usr/share/pixmaps/*
mkdir usr/share/ebookcreator/bin
mkdir usr/share/ebookcreator/themes
mkdir usr/share/ebookcreator/sources
mkdir usr/share/ebookcreator/books
cp -r dist/main/* usr/share/ebookcreator/bin
cp -r themes/* usr/share/ebookcreator/themes
cp images/logo.png usr/share/pixmaps
mv usr/share/ebookcreator/bin/main usr/share/ebookcreator/bin/EbookCreator

cd ..
dpkg -b ./ebookcreator ebookcreator.deb
cd ebookcreator