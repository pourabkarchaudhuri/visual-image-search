# Visual Image Search


![](http://yusukematsui.me/project/sis/img/screencapture2.jpg)

## Workflow
![](http://yusukematsui.me/project/sis/img/overview.jpg)

## Overview
- *Vis* is a simple image-based image search engine using Keras + Flask. You can launch the search engine just by running two python scripts.
- `offline.py`: This script extracts deep features from images. Given a set of database images, a 4096D fc6-feature is extracted for each image using the VGG16 network with ImageNet pre-trained weights.
- `server.py`: This script runs a web-server. You can send your query image to the server via a Flask web-intereface. Then relevant images to the query are retrieved by the simple nearest neighbor search.
- On an aws-ec2 instance with t2.large, the feature extraction takes 0.9 s per image. The search for 1000 images takes 10 ms. We tested Vis on Ubuntu 16.04 with Python3 and also on Win10 with Python3.


### Technology

VIS uses a number of open source projects to work properly:

* [Tensorflow] - A google open-source ML framework
* [Python] - awesome language we love

### Environment Setup

##### This was built on Windows 10.

These were the pre-requisities :

##### NVIDIA CUDA Toolkit
* [CUDA] - parallel computing platform and programming model developed by NVIDIA for general computing on graphical processing units (GPUs). Download and Install all the patches. During install, choose Custom and uncheck the Visual Studio Integration checkbox.

##### Download cuDNN
* [cuDNN] - The NVIDIA CUDA® Deep Neural Network library (cuDNN) is a GPU-accelerated library of primitives for deep neural networks. Create a NVIDIA developer account to download.

##### Set Path :
Add the following paths,
&nbsp;
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\bin
&nbsp;
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\libnvvp
&nbsp;
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\bin\extras\CUPTI\libx64

##### Install [Anaconda](https://www.anaconda.com/download/) with 3.6 x64

```sh
$ conda update conda
```

##### Run package installer

```sh
$ pip install -r requirements.txt
```

##### Install C/C++ Build tools

* [C/C++ Build Tools] - Custom librarires required to build C based implementations to Python runnable builds


## Usage
```bash
# Clone the code and install libraries
$ git clone https://github.com/pourabkarchaudhuri/visual-image-search.git
$ cd sis
$ pip install -r requirements.txt

# Put your image files (*.jpg) on static/img

$ python offline.py
# Then fc6 features are extracted and saved on static/feature
# Note that it takes time for the first time because Keras downloads the VGG weights.

$ python server.py
# Now you can do the search via localhost:5000
```

## Testing via APIs

----
  Returns json data about similar matches.

* **URL**

  /recognize

* **Method:**

  `POST`
  
*  **Headers**

   **Required:**
 
   `Content-Type=application/json`

* **Data Params**

  `{ "image_string": "BASE64_OF_IMAGE" }`

* **Sample Response:**

  ```javascript
    {
    "details": [
        {
            "name": "farmhouse_TableLamp4",
            "path": "http://localhost:5000/static/img/farmhouse_TableLamp4.jpg",
            "score": "0.8868542"
        },
        {
            "name": "farmhouse_TableLamp5",
            "path": "http://localhost:5000/static/img/farmhouse_TableLamp5.jpg",
            "score": "0.93646115"
        },
        {
            "name": "traditional_TableLamp7",
            "path": "http://localhost:5000/static/img/traditional_TableLamp7.jpg",
            "score": "0.9399547"
        }
     ]
  }
  ```

## Launch on AWS EC2
- You can easily launch Sis on AWS EC2 as follows. Note that the following configuration is just for the demo purpose, which would not be secure.
- To run the server on AWS, please first open the port 5000 and launch an EC2 instance. Note that you can create a security group such that port 5000 is opened.
- A middle-level CPU instance is fine, e.g., m5.large.
- After you log in the instance by ssh, the easist way to setup the environment is to use anaconda:
```bash
$ wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh
$ bash Anaconda3-5.3.1-Linux-x86_64.sh # Say yes for all settings
$ source ~/.bashrc  # Activate anaconda
```
- You might need to use python3.6 because currently tensorflow doesn't support 3.7: `conda install python=3.6`. Otherwise please create a new conda environment with python=3.6.
- Then let's run the commands in the above usage section.
- After you run `$ python server.py`, you can access the system via `http://ec2-XX-XX-XXX-XXX.us-west-2.compute.amazonaws.com:5000`
- (Advanced) If you'd like to deploy the system properly, please consider to run the Sis with the usual web server, e.g., uWSGI + nginx.



   [Tensorflow]: <https://www.tensorflow.org/>
   [Python]: <https://www.python.org/>
   [Anaconda]: <https://www.anaconda.com/download/>
   [CUDA]: <https://developer.nvidia.com/cuda-90-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exelocal>
   [cuDNN]: <https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.0.5/prod/9.0_20171129/cudnn-9.0-windows10-x64-v7>
   [Pretrained Model]: <https://drive.google.com/open?id=1sOMaZYWyWJJKJkQFVf3TUTX6-1iyR-kV>
   [C/C++ Build Tools]: <https://go.microsoft.com/fwlink/?LinkId=691126>
  
