# CS361-Microservice

The microservice features a web scraper that scrapes information from youtube videos about bicyle repairs and filters the information, 
providing a list of video ids and titles.

How to request data: In order to run the program, download all of the files in the Microservice folder, open them in a source code editor, such as Visual Studio Code,
and run npm install to install the necessary node modules. Migrate to scraper.js and type in the command npm start in your terminal. 
The filtered data will be displayed at http://localhost:3000/. 

How to receive data: An example command using the fetch api has been implemented in the file app.js. A fetch or get request will need to be implemented into the
backend part of the web app to get the data from the web server. To run app.js, type the command node app.js into your terminal, and the data will show up in 
the terminal. 

UML Sequence Diagram: 


![UML Diagram vpd](https://user-images.githubusercontent.com/86132170/180881923-c04a699a-9d36-4c3a-8d02-0741a26ed13a.png)
