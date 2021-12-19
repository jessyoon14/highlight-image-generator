# highlight-image-generator

Note: our system is tested on the Ubuntu 18.04 LTS, and hardware spec: intel i5-10400F, GTX1650 

To use our application, you should clone 3 GitHub repositories.

1. [Highlight image generator](https://github.com/jessyoon14/highlight-image-generator) (Back-end)
2. [VisualVoice](https://github.com/facebookresearch/VisualVoice) (Speech separation model - this directory should be cloned inside highlight-image-generator)
3. [Highlight image generator web](https://github.com/navy3690/highlight-image-generator-web) (Front-end)

To perform this, please type below command on the shell.

We set our environment by using conda with python version 3.8.12. If you want make same virtual environment, type below:

```bash
conda create --name test python=3.8.12
conda activate test
```

 After, clone the repositories and install requirement with below command:

```bash
mkdir highlight && cd highlight
git clone https://github.com/jessyoon14/highlight-image-generator
git clone https://github.com/navy3690/highlight-image-generator-web
cd highlight-image-generator
git clone https://github.com/facebookresearch/VisualVoice
mkdir -p media/audio media/audio_result media/image_result media/video

# install requirements for model and back-end
pip install -r requirements.txt

# install npm for front-end
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash 
source ~/.bashrc
conda activate test
nvm install v13.7.0
# install front-end dependencies
npm install --global yarn
yarn install
```

Below command are needed to resolve codec problem of the ffmpeg. If below command doesn’t work well, please refer [ffmpeg official installation guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu).

```cpp
sudo apt-get update -qq && sudo apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git-core \
  libass-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libmp3lame-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  meson \
  ninja-build \
  pkg-config \
  texinfo \
  wget \
  yasm \
  zlib1g-dev

sudo apt-get install libx264-dev
```

And, download pre-trained model.

```bash
# from inside the highlight-image-generator directory
mkdir -p VisualVoice/pretrained_models
cd VisualVoice/pretrained_models
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/facial_best.pth
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/lipreading_best.pth
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/unet_best.pth
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/vocal_best.pth
```

We use Microsoft Azure Cognitige Services: Speech-toText API. This API requires private key to access, so we didn't uploaded our private key for security. To obtain a private key for the Microsoft Azure API, please register to use this API by following [the official guide](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/overview#try-the-speech-service-for-free). After you initialize the Azure resource and obtain the private key, create the .env file by copying .env.example, filling in the API private key and region, and changing the file name to .env. Please note that Microsoft Azure offers a 30 day free trial period.


Serve the back-end server.

*Note: you must run **manage.py** in this directory. Our system uses relative path from the working directory, so please make certain that your current working directory is the ‘highlight’.*

```bash
# cd into this repository's directory, using the appropriate path for your computer
cd highlight-image-generator
python highlighter/manage.py runserver 8000
```

Please serve the front-end in another shell.

```bash
# cd into the frontend directory cloned above, using the appropriate path for your computer
cd highlight-image-generator-web
npm run serve
```

Now you can access our application! Please enjoy our application and try with your video!

Here are some video examples you can try:
1. Trump vs. Biden presidential debate
    1. https://www.youtube.com/watch?v=MOsW3cj53FI
    2. From 00:11 to 00:55
2. Robert Downey Jr. & Tom Holland on Spider-Man: Homecoming
    1. https://www.youtube.com/watch?v=2G-B5upjLjM
    2. From 00:54 to 1:02
3. Timothee Chalamet and Zendaya Buzzfeed Interview
    1. https://www.youtube.com/watch?v=ISpsfZxhnbs
    2. From 2:48 to 3:04
4. Pewdie pie and Marzia
    1. https://www.youtube.com/watch?v=78IfMhVFBLk
    2. From 3:58 to 4:20
5. Tom holland interview with Jimmy Fallon
    1. https://www.youtube.com/watch?v=hP8dOUm2qgc
    2. From 2:53 to 3:13
6. Timothee Chalamet and Zendaya Glamour Interview
    1. https://youtu.be/V7g2HSy3Pss
    2. From 4:35 to 4:45
