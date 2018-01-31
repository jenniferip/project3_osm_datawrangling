# Wrangling London OpenStreetMap Data Project

`/osm_project` is a folder containing the files used audit and clean OSM XML data from Mapzen's metro extracts. It also contains files to convert the data into dictionaries with a particular schema, validate the schema, and then create csv files to create and insert into my own queriable database, called 'london_osm.db'. Finally, it also holds files with SQL queries meant to explore our database and then files to run those queries. All queries are run using sqlite3.

Additionally, much of the code is credited to Udacitys' OpenStreetMap Case Study lesson and quizzes so there is code taken from that not written by myself mixed with also code written by myself that was originally written as solutions to quizzes. Finally, the `.html` file is inspired by the sample project provided by Carl Ward.  

** Note: ** Due to Github's space limitations, the following files are not included: `london_data.osm`, `london_sample.osm`, `ways_tags.csv`, and `ways_nodes.csv`. You may obtain my original London OSM extract through OpenStreetMaps metro data extract feature and then build the sample and csv files using the appropriate files below.

### Files

The files included are: 
* `london_data.osm` - this is the original download from Mapzen
* `london_sample.osm` - this file is a sample of the original data; created when you run the `sample_osm.py` file 
* `sampling_osm.py` - use this file to create a sample of the London data
* `users.py` - python file to find the number of unique users in the sample data
* `count_tags.py` - file to get an overview of the tags you see and how many of each you see
* `key_types.py` - this file gives a dictionary of potentially problematic values for an element's k attribute
* `audit.py` - this file audit's and fixes problematic street types
* `data.py` - this file reads in the sample data and writes it to csv files; note, this file works slowly and it gets more slower the bigger your data file is
* `schema.py` - file defining the schema of the dictionaries needed to create the csv files
* `create_and_fill_db.py` - executes the drop and create tables from `populate_db.sql` and then fills those tables with the data from the csv files created with `data.py`
* `explore.py` - executes and prints the results from the queries in `explore.sql`
* `populate_db.sql` - a list of drop and create queries to be executed by `create_and_fill_db.py`
* `explore.sql` - a list of the exploratory queries I ran on my database
* `nodes.csv` - file created by `data.py` containing the information from node elements
* `nodes_tags.csv` - file containing information from tags which are node children, created in `data.py`
* `ways.csv` - data from way elements, created in `data.py`
* `ways_tags.csv` - information from tags that are children of ways, created in `data.py`
* `ways_nodes.csv` - created in `data.py`, contains information from nodes that are children of ways
* `London_OSM_Analysis.html` - this is the jupyter notebook in which I describe and analyze my process and database
* `README.md`


### How to run

To run any particular **Python** file on your own, you will not need to run any other type of file, you must download the whole project and make sure you are in the project folder in your shell window. Then use the following, general command to run a file, `python filename.py`

Things to note:

a) If you want cannot download the data from my export, the html file holds instructions on where and how I downloaded my data.
b) `schema.py` does not do anything for you, the user, it is solely used by another file. You can run it but do not be surprised when it does nothing. 
c) Feel free to add your own queries to the `explore.sql` file, currently it contains those that I created to learn more about the data.
d) The following files need to be run in the following order:
 1) `sampling_osm.py` is **always** first it creates the sample which all other files use
 2) `users.py`, `count_tags.py`, and `key_types.py` can be run anytime after the sample is created. In fact, since sampling is pretty quick you can generate samples after the fact and run these files on the larger files to get further insight on the data. **Make sure the sample is small enough when you come to running `data.py` to keep time efficient!** 
 3) `audit.py` should logically be run after sampling and before `data.py` so that you clean the data before creating your csv files. **You do not want csv files containing erroneous or problematic data!**
 4) `data.py`, creates your csv files and it is the slowest to run so ideally you would only want to run this once on a sample data file of a good enough size!
 5) `create_and_fill_db.py`, always to be run after `data.py` as it creates the database and fills it with the information in the csv tables created by `data.py`.
 6) `explore.py`, the fun file. Executes SQL queries on the database last created by `create_and_fill_db.py` so it needs to be run after creating the database, otherwise you will get empty answers to your queries. 
