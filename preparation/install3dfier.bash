

sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo add-apt-repository universe
sudo apt update

sudo apt install build-essential

sudo apt install libcgal-dev
sudo apt install libboost-all-dev
sudo apt install libyaml-cpp-dev
sudo apt install libgdal-dev

sudo apt install -y unzip cmake

wget  http://lastools.github.io/download/LAStools.zip
unzip LAStools.zip
cd LAStools; mv LASlib/src/LASlib-config.cmake LASlib/src/laslib-config.cmake
mkdir build; cd build
cmake ..
sudo make install

cd ..

git clone https://github.com/tudelft3d/3dfier.git
cd 3dfier; mkdir build; cd build
cmake ..
sudo make install

