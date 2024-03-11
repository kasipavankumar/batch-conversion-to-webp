'''
    Script to convert all the images from
    common formats like jpg, png, jpeg to
    next gen WebP format.

    Make sure to have the following utility added
    to your system path.

    WebP Libraries:
    https://developers.google.com/speed/webp/docs/precompiled

    Refer:
    https://web.dev/codelab-serve-images-webp

    @author thekman
    @version 1.0
'''

# Required packages
import os                       # For OS level commands
import subprocess               # For executing bash commands
import shutil                   # For moving files
from os.path import splitext    # To seperate filename & its extension
from time import perf_counter   # To measure the execution time
import sys                      # To take params input from command line

# Global variables
dir_name = 'webp'                       # Directory name for WebP images
extensions = ('.png', '.jpg', '.jpeg')  # Image file extensions to convert
converted_extension = '.webp'           # Extension for converted WebP images

# Function to get all the images from a given directory
def get_images(directory, extensions=extensions):
    try:
        list_of_images = os.listdir(directory)
        images = list()

        for image in list_of_images:
            if image.endswith(extensions):
                images.append(os.path.join(directory, image))

        return(images)
    except:
        pass

# Function to convert the images to WebP format 
def convert_to_webp(image, directory):
    print('Converting {}...'.format(image))
    try:
        quality = 80
        filename, extension = os.path.basename(image), os.path.splitext(image)[1]
        filename_without_extension = filename.replace(extension, '')
        command = 'cwebp -q {} "{}" -o "{}.webp"'.format(quality, image, os.path.join(directory, filename_without_extension))
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()

    except:
        pass

# Function to move the webp images to a new folder
def move_webp_images(directory):
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(os.path.join(directory, dir_name)):
            os.mkdir(os.path.join(directory, dir_name))

        # Get all the images with .webp extension and move them to a new folder
        for image in os.listdir(directory):
            if image.endswith('.webp'):
                shutil.move(os.path.join(directory, image), os.path.join(directory, dir_name))
    except:
        pass

# Function to search for any missing images from the converted images directory
def get_missing_images_from_new_directory(directory):
    try:
        # Update the usage of get_images()
        list_of_original_images = get_images(directory)
        if(os.path.exists(os.path.join(directory, dir_name))):
            list_of_converted_images = os.listdir(os.path.join(directory, dir_name))

            # Match the converted images list with the original list to search for any missing images
            converted_images = set([os.path.splitext(filename)[0] for filename in list_of_converted_images if filename.endswith('.webp')])

            missing_images = [filename for filename in set(list_of_original_images) if os.path.splitext(filename)[0] not in converted_images]

            if(len(missing_images) > 0):
                return(missing_images)
    except Exception as e:
        print(e)

# This function checks if the missing images
# exist in the current (original) directory.
def if_missing_images_exist():
    try:
        missing_images = get_missing_images_from_new_directory()

        webp_images_in_curdir = [image for image in os.listdir(os.curdir)
                            if image.endswith('.webp')]

        converted_images_in_curdir = list(set([splitext(filename)[0]
                            for filename in webp_images_in_curdir]))

        missing_images_in_curdir = [filename.split('.')[0] for filename in set(missing_images)
                            if splitext(filename)[0] 
                            in converted_images_in_curdir]
        
        if(len(missing_images_in_curdir) > 0):
            return(True)
    except:
        pass

# Restore the missing images
def restore(directory):
    try:
        if(get_missing_images_from_new_directory(directory) is not None):
            for image in get_missing_images_from_new_directory(directory):
                convert_to_webp(image, directory)
    except Exception as e:
        print(e)

# Function to check if there are any images in the directory
def if_images_exist(directory):
    images = get_images(directory)
    if images is None:
        return 'Error: Unable to retrieve images'
    elif len(images) == 0:
        return 'No images'

# Function to check if all the images are already converted to WebP
def if_images_converted(directory):
    if_all_images_exist = get_images(os.path.join(directory, dir_name), converted_extension)
    if if_all_images_exist is None:
        return 'Unable to get all images exists'
    elif((len(get_images(directory)) == len(if_all_images_exist)) and (len(get_images(directory)) > 0) and (len(if_all_images_exist) > 0)):
        return('Images already exist')
    return('Missing Images')


def main(directory):

    # Check if there are any images
    if(if_images_exist(directory) == 'No images'):
        print('There are no images in the current directory.')
        input('\nPress any key to exit ')
        return
    else:

        # Check if all the images are already converted before performing the operation
        if(if_images_converted(directory) == 'Images already exist'):
            print('All the images exist in WebP format.')
            input('\nPress any key to exit ')
            return

        elif(if_images_converted(directory) == 'Missing images'):
            if(type(get_missing_images_from_new_directory(directory)) is list):
                if(if_missing_images_exist(directory) is True):
                    print('The converted images already exist in the original directory, moving them to the {}...'.format(dir_name))
                    start = perf_counter()

                    move_webp_images(directory)
                    
                    elapsed = perf_counter() - start
                    print('\nSuccessfully moved the images in {0:.4f}s'.format(elapsed))
                    input('\nPress any key to exit ')
                else:
                    print('Restoring the missing images...\n')
                    start = perf_counter()

                    restore(directory)
                    move_webp_images(directory)

                    elapsed = perf_counter() - start
                    print('\nSuccessfully restored the missing images in {0:.4f}s'.format(elapsed))
                    input('\nPress any key to exit ')

        # When images are not converted, convert to WebP & then move them to a new folder
        else:
            start_time = perf_counter()
            length_of_get_images = get_images(directory)
            if length_of_get_images is None:
                return 'Error: Unable to retrieve images'
            elif(len(get_images(directory)) > 0):
                for image in get_images(directory):
                    convert_to_webp(image, directory)

            move_webp_images(directory)

            elapsed_time = perf_counter() - start_time
            print('\nTask completed in {0:.4f}s'.format(elapsed_time))
            input('\nPress any key to exit ')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print(f'Usage: python convert_to_webp.py <directory>\nDefault path is Current directory: {os.getcwd()}')
        main(os.getcwd())
