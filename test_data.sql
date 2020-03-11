-- Data prepapred by Cecilia Wei, ywei2@ualberta.ca
-- and updated by Davood Rafiei, drafiei@ualberta.ca
-- Published on Jan 31, 2020

-- Let's insert some tuples to our tables. This is just an initial set and 
-- we definitly need more data for testing our queries.

insert into users values ('mc@gmail.com','Michael Choi','abcd','Edmonton, AB','M');
insert into users values ('tedwalsh@td.com','Ted Walsh','7632','Calgary, Ab','M');
insert into users values ('hm@mah.com','Harry Mah','1453','Waterloo, ON','M');
insert into users values ('ks@gmail.com','Kaitlyn Scott','pqwe','Toronto, ON','F');
insert into users values ('angels@gmail.com','Angel Silverman','anlo','Vancouver, BC','F');
insert into users values ('mk@abc.com','Maximillion Kung','0931','Burnaby, BY','F');
insert into users values ('davood@gmail.com','Davood Rafiei','1234','Edmonton, AB','M');


insert into products values ('N01', 'Nikon F100');
insert into products values ('N02', 'Nikon D3500');
insert into products values ('B01', 'BMW M8');
insert into products values ('P01', 'Porsche 911');
insert into products values ('P02', 'Porsche 918');

insert into sales values ('S01', 'mc@gmail.com', 'N01', '2020-03-24', 'Camera Sale', 'Brand new', 1400);
insert into sales values ('S02', 'mc@gmail.com', 'N02', '2020-09-02', 'Great deal', 'Used', 698);
insert into sales values ('S03', 'hm@mah.com', 'N02', '2020-12-12', 'End year', 'New', 530);
insert into sales values ('S04', 'ks@gmail.com', 'P01', '2020-03-14', 'Amazing', 'New', 30000000);

insert into bids values ('B01', 'hm@mah.com', 'S01', '2016-04-01', 1405.02);
insert into bids values ('B02', 'ks@gmail.com', 'S01', '2016-04-02', 1407.99);
insert into bids values ('B03', 'hm@mah.com', 'S02', '2018-09-11', 999);
insert into bids values ('B04', 'angels@gmail.com', 'S03', '2016-01-03', 430);
insert into bids values ('B05', 'tedwalsh@td.com', 'S04', '2019-05-19', 39099999);


insert into reviews values ('mc@gmail.com', 'tedwalsh@td.com', 4.9, 'great guy!', '2016-05-02');
insert into reviews values ('hm@mah.com', 'ks@gmail.com', 5.0, 'car is amazing', '2015-09-02');
insert into reviews values ('angels@gmail.com', 'mc@gmail.com', 0.5, '', date('now','-4 years'));


insert into previews values (1, 'N01', 'hm@mah.com', 1.5, 'definitly used', '2016-04-25');
insert into previews values (2, 'N02','ks@gmail.com', 2, 'great quality', '2018-09-11');
insert into previews values (4, 'N02','hm@mah.com', 3, 'great quality', '2019-09-11');
insert into previews values (3, 'P02', 'mk@abc.com', 5, 'amazing car', date('now','-9 months'));



