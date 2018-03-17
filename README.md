# Project 4: Item Catalog for Udacity's Full Stack Developer Nanodegree
## ABOUT

An item catalog written primarily in Flask, SQLAlchemy, Bootstrap, and CSS which stores products in a database and displays them on a web page. Clients are able to delete, edit, and create new products.

## HOW TO USE

- Install [Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html)

- Download this repository into any computer directory.

- From your terminal, inside the ```vagrant``` subdirectory, run the command ```vagrant up```. This will cause Vagrant to download the Linux operating system and install it.

- When vagrant up is finished running, you will get your shell prompt back. At this point, you can run ```vagrant ssh``` to log in to your newly installed Linux VM!

- In the VM, type in ```cd /vagrant``` to access the files containing the Item Catalog.

- Once inside, run the command ```python lotsofitems.py``` fill the database.

- Afterward, run the command ```python itemcatalog.py``` to run the web app from localhost. 

- Finally, go into your preferred web browser and type in ```localhost:5000/categories/``` to view the contents inside. 

- Enjoy, explore, and maybe buy an item or two from their respective manufacturer!

## TOOLS USED

- Python 3.6 editor IDLE
- Flask
- SQLAlchemy
- Bootstrap
- HTML
- CSS
- Google Chrome
