create database battery_swap;
use battery_swap;
create table users (
	id int primary key auto_increment,
    username varchar(100),
    email varchar(100),
    password varchar(255)
);
create table appointments (
	booking_id int primary key auto_increment,
	user_id int,
	station varchar(100),
	date date,
    time time,
    status varchar(50),
    foreign key (user_id) references users(id)
);