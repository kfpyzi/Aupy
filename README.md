# Aupy

Auditing System using Python and Google APIs
This system was created to help a friend's friend in auditing the google drive files automatically into a Google spreadsheet.
I used python to experience in developing and accessing Google APIs

### Prerequisites

What things you need to install the software and how to install them:
In running the program you need to have these libraries which are available on pip.

- httplib2
```
pip install httplib2
```
- pydrive
```
pip install pydrive
```
- Google Spreadsheet
```
pip install gspread
```
- Google API for Python
```
pip install --upgrade google-api-python-client
```

## Deployment

In deploying this script
```
python main.py
```
The script will then authenticate through the browser for confirmation.
After confirmation, it will then audit the google drive of the user selected in confirming the app.

It will produce a csv file for the audited files in a format where the fields are:
Date Created, Date Last Modified, Title, Mime Type, Alternate Link, Folder Path, Owner Name

Sample Data Listed Below
```
b"2017-05-12T03:25:16.336Z	
2017-09-05T06:27:30.403Z	
Recruitment Directory 	
application/vnd.google-apps.spreadsheet	https://docs.google.com/a///edit?usp=drivesdk	
root> Recruitment Directory  	
['CEP']" 																			
```
Screenshot of a sample Command Prompt in writing to the Google Sheet

<img src="https://farm2.staticflickr.com/1830/42919111692_3f296000fc.jpg" width="500" height="366" alt="4">

Screenshot of a sample Google Sheet Produced

<img src="https://farm2.staticflickr.com/1774/41158390800_b351fa5240.jpg" width="500" height="281" alt="5">

## Built With

* [Google API Python](https://developers.google.com/sheets/api/quickstart/python)
* [GSpread by burnash](https://github.com/burnash/gspread)

## Authors

* **Kyle Farinas** - [kfpyzi](https://github.com/kfpyzi)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* To the friend who introduced me to her friend to make this project.
* Google Quickstart API, you the best.

