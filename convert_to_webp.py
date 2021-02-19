'''
    Script to convert all the images from
    common formats like jpg, png to
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

import os                       # For OS level commands
import subprocess               # For executing bash commands
import shutil                   # For moving files
from os.path import splitext    # To seperate filename & its extension
from time import perf_counter   # To measure the execution time

# Global namespace
dir_name = 'webp'
any_missing_images = False
extensions = ('.png', '.jpg', '.jpeg')
are_images_converted = os.path.exists(os.path.join(os.curdir, dir_name))

# Function to get all the images from a given directory
def get_images():
    try:
        list_of_images = os.listdir(os.curdir)
        images = list()

        for image in list_of_images:
            if image.endswith(extensions):
                images.append(image)

        return(images)
    except:
        pass

list_of_original_images = get_images()   

# Function to convert the images to WebP format 
# https://stackoverflow.com/a/48066158
def convert_to_webp(image):
        try:
            quality = 80
            filename, extension = image, image.split('.')[1]
            filename_without_extension = filename.replace(
                    '.{}'.format(extension), '')
            command = 'cwebp -q {} "{}" -o "{}.webp"'.format(
            quality, filename, filename_without_extension)
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            output, error = process.communicate()

        except:
            pass

# Function to move the webp images to a new folder
# https://stackoverflow.com/a/36091444
def move_webp_images():
    try:
        # Create the directory if only it doesn't exist
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        # If the directory exist,
        # get the list of images present in it & match it with the
        # original list
        else:
            pass

        # Get all the images with .webp extension
        # and move them to a new folder
        webp_ext = ('.webp')
        images = os.listdir(os.curdir)
        subFolder = os.path.join(os.curdir, dir_name)
        for image in images:
            if image.endswith(webp_ext):
                shutil.move(os.path.join(os.curdir, image), subFolder)
    except:
        pass

# Function to search for any missing images
# from the converted images directory.
def get_missing_images_from_new_directory():
    try:
        global any_missing_images

        if(os.path.exists(os.path.join(os.curdir, dir_name))):
            list_of_converted_images = os.listdir(
                                        os.path.join(os.curdir, dir_name))

            # Match the converted images list with the original
            # list to search for any missing images.
            # https://stackoverflow.com/a/33837822
            converted_images = set([splitext(filename)[0]
                                for filename in list_of_converted_images 
                                if filename.endswith('.webp')])

            missing_images = [filename for filename in set(list_of_original_images)
                                if splitext(filename)[0] not in converted_images]

            if(len(missing_images) > 0):
                any_missing_images = True
                return(missing_images)
            else:
                any_missing_images = False

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

# Restore the missing images.
def restore():
    try:
        if(get_missing_images_from_new_directory() != False):
            for image in get_missing_images_from_new_directory():
                convert_to_webp(image)
    except Exception as e:
        print(e)    

# Function to check if there are any images
# in the current directory
def if_images_exist():
    if(len(get_images()) == 0):
        return('No images')

# Function to check if all the images 
# are already converted to WebP
def if_images_converted():
    dir_name = 'webp'

    if os.path.exists(dir_name):
        if_all_images_exist = os.listdir(os.path.join(os.curdir, dir_name))

        if((len(get_images()) == len(if_all_images_exist) and
            (len(get_images()) > 0) and len(if_all_images_exist) > 0)):
            return('Images already exist')
        
        return('Missing images')

def main():

    # Check if there are any images
    if(if_images_exist() == 'No images'):
        print('There are no images in the current directory.')
        input('\nPress any key to exit ')
        return
    else:

        # Check if all the images are already converted
        # before performing the operation
        if(if_images_converted() == 'Images already exist'):
            print('All the images exist in WebP format.')
            input('\nPress any key to exit ')
            return

        elif(if_images_converted() == 'Missing images'):
            if(type(get_missing_images_from_new_directory()) is list):
                if(if_missing_images_exist() == True):
                    print('The converted images already exist in the original directory,', end = ' ')
                    print('moving them to the {}...'.format(dir_name))
                    start = perf_counter()

                    move_webp_images()
                    
                    elapsed = perf_counter() - start
                    print('\nSuccessfully moved the images in {0:.4f}s'.format(elapsed))
                    input('\nPress any key to exit ')
                else:
                    print('Restoring the missing images...\n')
                    start = perf_counter()

                    restore()
                    move_webp_images()

                    elapsed = perf_counter() - start
                    print('\nSuccessfully restored the missing images in {0:.4f}s'.format(elapsed))
                    input('\nPress any key to exit ')

        # When images are not converted,
        # Convert to WebP & then move them to a new folder
        else:
            start_time = perf_counter()
            if(len(get_images()) > 0):
                for image in get_images():
                    convert_to_webp(image)

            move_webp_images()

            elapsed_time = perf_counter() - start_time
            print('\nTask completed in {0:.4f}s'.format(elapsed_time))
            input('\nPress any key to exit ')

main()
