# Google-Drive-2-Photos using Openshift
A python script to Directly Transfer photos from Google drive -> Google photos Using Openshift

                         *(                
                         *(((              
                         *(((((            
                         *(((((((          
                *********/(((((((((        
              ,,,,*******/(((((((%%        
            ,,,,,,,,*****/(((((%%%%        
          ,,,,,,,,,,,,*** (((%%%%%%        
        ,,,,,,,,,,,,,,,,   %%%%%%%%        
                ((((((((   ((((((((((((((((
                ((((((/** ###((((((((((((  
                ((((/****/#####((((((((    
                ((/******/#######((((      
                /********/########(        
                  *******.                 
                    *****.                 
                      ***.                 

## Description

Google Drive  - Using the Drive API

Google Photos - Doesn't provide an API till date and this method is based
                on reverse-engineering the Google Photos Web Upload.

Hence for this to work ,the cookie of your drive account is needed and 
few details mentioned in INPUTS.json file.
  1. cookie - *Cookie of google photos account to which you wish to transfer photos*
  2. clientInfo - *Supplied by the google photo web upload to the google server*
  3. effective_id - *Denotes owner of the file on drive - owner_id*
  
This script will Download all images from Google Drive and uploads to Google Photos
```
Note :
This script can be hosted on Heroku or Openshift (Paas) which would be much faster 
if you have large number of photos or a crappy Internet Connection
```

## Requirements
1. Google Drive API - Enabled for your account
	* [Turn on the Drive API ](https://developers.google.com/drive/v3/web/quickstart/python#step_1_turn_on_the_api_name) : Follow the step one of Google Python Quickstart 
2. Python 2.7 or later  - *This is based on 2.7*
3. Git on windows/linux. 

 
## Installation
```python
python setup.py install
```

## Usage
##### Fork and clone a copy of this git repository
Getting the Required info for the first time.

Make Sure you got the DRIVE API Enabled and Downloaded the client_secret.json file
to the git repository.
  1. Open you Firefox browser and go to page photos.google.com and sign-in to your account
  2. Open the Firefox Dev Tools [Right click - Select ->Inspect Elements (or) Press *"Q"* from Keyboard]
  3. Go to the Network tab of Dev Tools
  4. Upload a sample image by dragging it over the browser window.
  5. In Network tab watch for a POST request "resumable?authuser=0"
  6. Follow the Screenshot images

![step 6](/screenshots/1.jpg?raw=true)
![step 7](/screenshots/2_.jpg?raw=true)

Save changes and update the repository

Finally run the following in (cmd/terminal):

```python
python app.py
```
  7. Obtain the Google Drive OAuth Credentials which will be saved in .credentials folder
  8. Upload the updated repository to Openshift for Direct Online transfer

## Using Openshift Hosting
* Create a Free account 
* [Getting Started with OpenShift Online](https://developers.openshift.com/getting-started/index.html)
* Create a New  Python App in the web console and during creation provide your git repository url 
or later Upload the git repository using ```rhc command line tool```

![openshift](/screenshots/openshift.jpg?raw=true)
* In the _rhc command-line tool_ type the command 
  ```
  rhc tail -a YOUR_APP_NAME
  ```
  to view logs

## Credits
 *Jagadeesan : myscoreisone@gmail.com*
 
## Bugs and Improvements
Make a Pull request / file an issue.

## License
The MIT License (MIT)
Copyright (c) 2016 Jagadeesan
