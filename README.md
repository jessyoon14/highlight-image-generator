# highlight-image-generator

Note: our system is tested on the Ubuntu 18.04 LTS, and hardware spec: intel i5-10400F, GTX1650 

To use our application, you should clone 3 GitHub repositories.

1. [Highlight image generator](https://github.com/jessyoon14/highlight-image-generator) (Back-end)
2. [VisualVoice](https://github.com/facebookresearch/VisualVoice) (Speech separation model - this directory should be cloned inside highlight-image-generator)
3. [Highlight image generator web](https://github.com/navy3690/highlight-image-generator-web) (Front-end)

To perform this, please type below command on the shell. In below example, we set root directory as '*~/highlight'* in this example command.

We set our environment by using conda with python version 3.8.12. If you want make same virtual environment, type below:

```bash
conda create --name test python=3.8.12
conda activate test
```

 After, clone the repositories and install requirement with below command:

```bash
mkdir -p ~/highlight && cd ~/highlight
git clone https://github.com/jessyoon14/highlight-image-generator
git clone https://github.com/navy3690/highlight-image-generator-web
cd highlight-image-generator
git clone https://github.com/facebookresearch/VisualVoice
mkdir media
mkdir -p media/audio && audio_result && image_result && video

# install requirements for model and back-end
pip install -r requirements.txt

# install npm for front-end
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash 
source ~/.bashrc
conda activate test
nvm install v13.6.0
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
mkdir -p ~/highlight/VisualVoice/pretrained_models
cd ~/highlight/VisualVoice/pretrained_models
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/facial_best.pth
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/lipreading_best.pth
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/unet_best.pth
wget http://dl.fbaipublicfiles.com/VisualVoice/av-speech-separation-model/vocal_best.pth
```

We use Microsoft Azure API. The API requires private key to access, so we didn't uploaded our private key for security. To activate Azure API, please register to Azure in the homepage, and write private key in *'.env'* file.

 

```bash
vim ~/highlight/highlight-image-generator/.env
# Write your Azure private key here
```

Turn on the back-end.

*Note: you must run **manage.py** in this directory. Our system uses relative path from the working directory, so please make certain that your current working directory is the ‘highlighter’.*

```bash
# cd into this repository's directory, using the appropriate path for your computer
cd ~/highlight-image-generator/highlighter
python manage.py runserver
```

Please turn on the front-end in another shell.

```bash
# cd into the frontend directory cloned above, using the appropriate path for your computer
cd ~/highlight/highlight-image-generator-web
npm run serve
```

Now you can access our application! Please enjoy our application and try with your video!
