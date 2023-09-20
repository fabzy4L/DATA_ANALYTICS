create table accounts (
	user_id serial primary key,
	username VARCHAR (50) unique not null,
	password VARCHAR (50) not null,
	email VARCHAR (255) unique not NULL
);

insert into accounts values
(1, 'Daniel', '1234', 'daniel@gmail.com');