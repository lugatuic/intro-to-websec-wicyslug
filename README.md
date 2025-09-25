# LUG X WiCyS - Intro to Web Security

For our first Cybersecurity themed workshop for the WiCyS X LUG Cybersecurity collab weeks!

## Table of Contents
- File Directory
- Instructions
  - Building Slides
  - Running the Server Locally

## File Directory

```
.
├── server
│   └── app
│       └── templates
└── slides
    ├── assets
    ├── out
    └── src
```


## Instructions

### Building Slides

This slide deck is built using `lug-template`.

Run `make all` while in the `slides` folder to build the slides. If you are having trouble building slides, please ensure you are building slides correctly and have all required prerequisites by reading the instructions [here](https://github.com/lugatuic/lug-template/blob/master/README.md#instructions).

### Running The Server Locally 

**DO NOT USE THIS SERVER IN A PRODUCTION ENVIROMENT. IT IS UNSAFE BY DESIGN. I WENT OUT OF MY WAY TO AVOID BUILT IN SECURITY MEASURES BY BOTH FLASK AND SQLITE3.**

Running this project requires you have `docker` installed.

To build the container image:
1. Navigate to the `server` directory.
2. Run `docker build -t IMAGE-NAME .` wherein "IMAGE-NAME" is whatever you call the docker image. I tend to use `insecure-server` or `insecure-server:lug`.
3. Run `docker run IMAGE-NAME` to run the container. By default, it will bind to your IP on port 80.  

NOTE: If you want to update any of the files within the `server` directory, you will need to rebuild the docker image. Additionally, docker images do not self prune, so if you are consistently building and running to test, I recommend to `docker system prune` inbetween builds.

Personally, I run
```
docker build -t insecure-server . \
docker system prune \
docker run insecure-server
```
