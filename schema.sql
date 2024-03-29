create table Selections(selectid integer PRIMARY key AUTOINCREMENT not null, supplement text not null, amount_per_serving integer,
unit text not null, percent_daily_value integer);

create table User(userid integer PRIMARY key AUTOINCREMENT not null, user_name text not null unique, password text not null);

create table Data(dataid integer PRIMARY key AUTOINCREMENT not null, supplement text, row_number integer, 
age_range text, male text, female text, pregnancy text, lactation, text);

create table Temp(tempid integer PRIMARY key AUTOINCREMENT not null, row_number integer not null, 
age_range text not null, male text not null, female text not null, pregnancy text, lactation, text);

insert into Data(supplement)
values
("Vitamin A"),
("Vitamin A"),
("Vitamin A"),
("Vitamin A"),
("Vitamin A"),
("Vitamin A"),
("Vitamin A"),
("Vitamin A"),
("Vitamin B6"),
("Vitamin B6"),
("Vitamin B6"),
("Vitamin B6"),
("Vitamin B6"),
("Vitamin B6"),
("Vitamin B6"),
("Vitamin B6"),
("Iron"),
("Iron"),
("Iron"),
("Iron"),
("Iron"),
("Iron"),
("Iron"),
("Iron"),
("Manganese"),
("Manganese"),
("Manganese"),
("Manganese"),
("Manganese"),
("Manganese"),
("Manganese"),
("Manganese"),
("Omega-3 Fatty Acids"),
("Omega-3 Fatty Acids"),
("Omega-3 Fatty Acids"),
("Omega-3 Fatty Acids"),
("Omega-3 Fatty Acids"),
("Omega-3 Fatty Acids"),
("Omega-3 Fatty Acids"),
("Omega-3 Fatty Acids"),
("Potassium"),
("Potassium"),
("Potassium"),
("Potassium"),
("Potassium"),
("Potassium"),
("Potassium"),
("Potassium"),
("Riboflavin"),
("Riboflavin"),
("Riboflavin"),
("Riboflavin"),
("Riboflavin"),
("Riboflavin"),
("Riboflavin"),
("Riboflavin"),
("Thiamin"),
("Thiamin"),
("Thiamin"),
("Thiamin"),
("Thiamin"),
("Thiamin"),
("Thiamin"),
("Thiamin"),
("Selenium"),
("Selenium"),
("Selenium"),
("Selenium"),
("Selenium"),
("Selenium"),
("Selenium"),
("Selenium");