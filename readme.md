# WebP Converter
## A Handy Python script that converts images to the WebP format.

It is always good to serve optimized & quality images on your website.
The WebP format is always recommended for everything web.

The aim of this script is to convert all your images in batch & organize them to a new directory.


## Why WebP?
WebP is the format developed with web in mind. It provides many performance benefits while serving the assets for your website. 

Reference: [web.dev](https://web.dev/serve-images-webp/)


## How the script works?
![Demo](demo/demo.webp "webp")

The script uses the [WebP library](https://developers.google.com/speed/webp/docs/precompiled) provided by Google for the conversion process.

You are required to copy the provided script to the directory where all your
images are being stored. Though not neccesary but suggested, that the directory should contain only the image files.

On running, the script will scan the current directory for images with extensions of '.jpg', '.jpeg' & '.png'. Next, using the following bash command, the script will convert the every selected image to '.webp' format.

Command: `cwebp -q 80 image.jpg -o image.webp`
where, 80 = typical output quality.

_Quality can be modified by editing the `quality` variable in the script._

Once converted, the images will be organized to a new directory named 'webp'.

_The name of the directory can be modified by editing the `dir_name` variable in the script._

**NOTE: Converted images will have the same name as they had before conversion.**


## Why this script?
The script is smart enough to:

* Detect for the missing images after conversion & restore them accordingly.
* Detect if the missing images are present in the original directory, it moves them accordingly and thus save you time by not converting existing images again.

More features are in progress.

## How to run this script?
1. Install the latest & stable version i.e., **3.8.1** of [Python](https://www.python.org/downloads/).
2. Download the [WebP library](https://developers.google.com/speed/webp/docs/precompiled) provided by Google. You can find the latest version i.e., **1.1.0** at bottom of the page.
3. Extract the compressed folder & add path of the bin directory to your system variables.
Path will look something like this: `..\libwebp-1.1.0-windows-x64\bin`
4. Enter `cwebp -version` in CLI, which will return the version number. This indicates a successful installation.
5. You are ready to copy the script & use it.

I hope you find this script useful, cheers!

---

`Code Plus Coffee`