#-------------------------------------------------------------------------------------------------
# Author(s): Josh Noble (jtn6092), Jennika Haining (jmh1592)
# Purpose: Upload .csv file with smart shed data to Dropbox
#
# TO-DO: Setup dropbox account for the smart shed
#	 Integrate with main.py
#	 Add function to delete old files from dropbox directory.
#	 - May not need if we just overwrite the old file
# 
# Setup Steps: (1) Create Dropbox account for shed. Share login info with team and add to this file.
#              (2) Install dropbox sdk: 'sudo pip install dropbox'
#              (3) Create app on Dropbox console (www.dropbox.com/developers). Generate token
#                  and update this file with the token and desired file paths.
#
# Note: Token set to never expire. May want to evaluate security risks and add auth steps.
# Access Token = 'cOosVB7gbxsAAAAAAAAAARCfIPLFPsWZ9ywvtdV6ElNo20CPaf_ySk-mBsIl82uU'
# Smart Shed Dropbox Account: Username='' Password=''
# This code is derivative work of Keshava11:
# https://gist.github.com/Keshava11/d14db1e22765e8de2670b8976f3c7efb
#-------------------------------------------------------------------------------------------------
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Define access token, local path, and dropbox path - CHANGE THIS
TOKEN = 'cOosVB7gbxsAAAAAAAAAARCfIPLFPsWZ9ywvtdV6ElNo20CPaf_ySk-mBsIl82uU'
LOCALFILE = '/Users/joshnoble/Downloads/MSD/test_doc.csv'
DB_PATH = '/test_doc123.csv'

# Upload LOCALFILE to Dropbox
def upload():
    with open(LOCALFILE, 'rb') as f:
        # WriteMode=overwrite used to overwrite files of the same name
        print("Uploading " + LOCALFILE + " to Dropbox as " + DB_PATH + "...")
        try:
            dbx.files_upload(f.read(), DB_PATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # Checks for error where user doesn't have enough Dropbox space to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient Dropbox storage.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


# Check file details
def checkFileDetails():
    print("Checking file details")

    for entry in dbx.files_list_folder('').entries:
        print("File list is : ")
        print(entry.name)

# Delete old files
def deleteOldFiles():
    print("Deleting files older than x days...")
    # Need to add code here


if __name__ == '__main__':
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token."
	         "Go to https://www.dropbox.com/developers/apps. Generate"
		 "a token in app settings and add it to line 24")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an"
		 "access token from the app console on the web.")

    #try:
    #    checkFileDetails()
    #except Error as err:
    #    sys.exit("Error while checking file details")

    print("Uploading the file...")
    # Upload the file to Dropbox
    upload()

    print("Upload successful!")
