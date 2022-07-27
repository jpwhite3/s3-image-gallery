# S3 Image Gallery

This is a simple tool that will render a static HTML web-gallery for a given directory of images. It will generate thumbnails as it copies files to the target directory. Because it is making an extra copy, this could be expensive in terms of storage & I/O while a build is running - especially with large galleries.

Once complete, the `dist` directory will contain the static content and images copied. Upload the contents of this content to any webserver to host. You can test this locally by running `make run`

![alt tag](https://raw.githubusercontent.com/jpwhite3/s3-image-gallery/main/example.jpg)

# Build Instructions

## Prerequisites

- You are running in a unix-like environment (Linux, MacOS)
- Python 3.6 or higher (`python3 --version`)
- poetry installed (`pip install -U poetry`)

## Setup

```bash
make bootstrap
```

## Test

```bash
make test  # Creates content at ./dist/ from ./test/
```

## Build

```bash
make GALLERY_DIR=/some/place build  # Creates content at ./dist/ from /some/place
```

## Run local server

```bash
make GALLERY_DIR=/some/place run  # Hosts content at ./dist/ from /some/place
```
