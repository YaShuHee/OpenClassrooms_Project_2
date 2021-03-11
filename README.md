# [EN] [Books to scrape](https://books.toscrape.com) scraping Python script

## Features
* Scrape a product page from the [Books to scrape](https://books.toscrape.com) website using BeautifulSoup4.

* Implement an ETL (extract - transform - load) process :
    1. Extract the data from the page.    
    2. Transform the data so they fit the CSV file format.
    3. Write a CSV with following characteristics :
        1. Columns are the following (in this order) :
            * product_page_url,
            * universal_product_code,
            * title,
            * price_including_tax,
            * price_excluding_tax,
            * number_available,
            * product_description,
            * category,
            * review_rating,
            * image_url.
        2. Columns are separated by commas.
        3. There is only one data record/line of fields (one product).
        4. Fields are separated by commas.
        5. Fields are delimited by double-quotes (double-quotes inside fields are escaped by being replaced by two double-quotes).

* When running the main.py script, a terminal dialog let you chose if you want to generate a CSV file with the scraped data, and the file name and directory.

* The created CSV files can be opened with Libre Office Calc, Microsoft Office Excel or any CSV file reader/editor.


<br><br><br>
## User instructions
Just run the main.py script with python, by running this command from the project 's root :
```shell script
python3 ./src/main.py
```

<br><br><br>
## Installation

### Download the source (and unzip it if needed)
Download the source code using one of the three following ways :
* Click on this [link](https://github.com/YaShuHee/OpenClassrooms_Project_2/archive/production.zip) and unzip the downloaded archive.
* From Github, click on "Code > Download ZIP" and unzip the downloaded archive.
* After installing [Git](https://git-scm.com/downloads), clone it with the command :
    ```shell script
    git clone https://github.com/YaShuHee/OpenClassrooms_Project_2
    ```

<br><br>
### Environment configuration

#### Install Python3
Install [Python3](https://www.python.org/downloads/) on your computer (version 3.7 or later).


#### Create a Python3 virtual environment
Run this command from inside the "OpenClassrooms_Project_2" directory you unzipped sooner :
```shell script
python3 -m venv env
```
It will create a directory named "env", including a full Python3 virtual environment, totally independant from your main Python3 installation, having its own installed packages.

* On Windows :
    You can now activate your virtual environment to use it (to execute code and to modify installed packages on it) by running the following command :
    ```shell script
    . .\env\Scripts\activate
    ```

* On Linux/MacOS :
    You must make the environment activation script executable (only once), by typing the following command :
    ```shell script
    sudo chmod +x ./bin/activate
    ```
    You can now activate your virtual environment to use it (to execute code and to modify installed packages on it) by running the following command :
    ```shell script
    . ./env/bin/activate
    ```
 To exit the virtual environment without exiting your commandline, run this :
 ```shell script
deactivate
```

#### Install requirements
Activate the virtual environment you just installed with the previously mentionned command :
* On Windows
    ```shell script
    . .\env\Scripts\activate
    ```
* On Linux/MacOS :
    ```shell script
    . ./env/bin/activate
    ```
Now (still from the project root), run :
```shell script
pip install -r requirements.txt
```
Congratulations !
Your virtual environment is fully installed.
From now, whenever you want to run the project, just activate your environment and follow the [User instructions](#user-instructions).