-- Data prepared by Natalie Iwaniuk, niwaniuk@ualberta,ca
-- Published on February 07 2020, updated February 13 2020


insert into users values ('ibev@gmail.com','Ivan Beverly','password','Edmonton','M');
insert into users values ('rupertd@yahoo.ca', 'Rupert Das', 'qwerty', 'Waterloo', 'M');
insert into users values ('abanner@ualberta.ca', 'Andrea Banner', 'aeiouy', 'Calgary', 'F');
insert into users values ('justhereforfun@live.ca', 'Anony Mouse', 'nope', 'Vancouver', 'M');
insert into users values ('jeansantiago@hotmail.com', 'Jeannette Santiago', 'jjsan', 'Edmonton', 'F');
insert into users values ('myonlysunshine@outlook.com', 'Klara Sunshine', '1989baby!', 'Calgary', 'F');
insert into users values ('teeltheburn@gmail.com', 'Patrick Teel', 'whoami1', 'Vancouver', 'M');
insert into users values ('mattress@mattress.com', 'Dave Mattress', 'mattress', 'Edmonton', 'M');


insert into products values ('G01', 'Galaxyland Ticket');
insert into products values ('X01', 'XBox One');
insert into products values ('X02', 'XBox 360');
insert into products values ('M01', 'Movie Ticket');
insert into products values ('M02', 'Free Movie Voucher');
insert into products values ('P01', 'Playstation 4');
insert into products values ('P02', 'Playstation 3');
insert into products values ('C01', 'Canon Tx3000');
insert into products values ('M03', 'Mattress');


insert into sales values ('S01', 'ibev@gmail.com', 'G01', date('now', '+3 days'), 'ticket for indoor amusement park!', 'Brand new', 50);
insert into sales values ('S02', 'ibev@gmail.com', 'M02', '2020-02-01', 'Cineplex Voucher (VIP)', 'Brand new', 5);
insert into sales values ('S03', 'abanner@ualberta.ca', 'P01', date('now', '+7 days'), 'First Generation PS4', 'Used', 200);
insert into sales values ('S04', 'rupertd@yahoo.ca', 'M01', date('now', '-1 day'), 'back centre seat ticket for movie!', 'New', 10);
insert into sales values ('S05', 'jeansantiago@hotmail.com', 'C01', date('now', '-1 day'), 'poster printer, comes with ink!', 'Used', 1500.50);
insert into sales values ('S06', 'rupertd@yahoo.ca', 'X01', date('now', '-2 days'), 'brand new xbox one s', 'Brand new', 399.99);
insert into sales values ('S07', 'ibev@gmail.com', 'X02', '2020-02-20', 'xBox 360 signed by bungie', 'New', 900.00);
insert into sales values ('S08', 'rupertd@yahoo.ca', 'X02', date('now', '-2 days'), 'generation 1 XBox 360', 'Used', 299.98);
insert into sales values ('S09', 'jeansantiago@hotmail.com', 'P01', '2020-02-18', 'ps4 for sale', 'Used', 250.00);
insert into sales values ('S10', 'justhereforfun@live.ca', 'P01', date('now', '+1 day'), 'totally not stolen PS4', 'Brand new', 150.99);
insert into sales values ('S11', 'justhereforfun@live.ca', 'P01', '2020-01-30', 'the best PS4 ever seen in ever time', 'Brand new', 450000000);
insert into sales values ('S12', 'rupertd@yahoo.ca', 'X02', date('now', '-1 day'), 'special edition xbox 360', 'New', 300);
insert into sales values('S13', 'mattress@mattress.com', 'M03', date('now', '-3 days'), 'mattress', 'New', 400);
insert into sales values ('S14', 'mattress@mattress.com', 'M03', date('now', '+1 day'), 'comfy comfy mattress', 'Used', 400);
insert into sales values ('S15', 'mattress@mattress.com', 'M03', date('now', '-10 days'), 'best values', 'Brand new', 600);
insert into sales values ('S16', 'mattress@mattress.com', 'M03', date('now', '+4 days'), 'amazing mattress', 'Used', 900);
insert into sales values ('S17', 'mattress@mattress.com', 'M03', date('now', '-3 days'), 'great', 'Brand new', 500);


insert into bids values ('B01', 'rupertd@yahoo.ca', 'S01', date('now', '+1 day'), 20);
insert into bids values ('B02', 'jeansantiago@hotmail.com', 'S01', date('now', '+1 day'), 50);
insert into bids values ('B03', 'rupertd@yahoo.ca', 'S01', date('now', '+2 days'), 55);
insert into bids values ('B04', 'jeansantiago@hotmail.com', 'S08', date('now', '-3 days'), 300);
insert into bids values ('B05', 'jeansantiago@hotmail.com', 'S07', '2020-02-19', 850);
insert into bids values ('B06', 'jeansantiago@hotmail.com', 'S06', date('now', '-3 days'), 400);
insert into bids values ('B07', 'teeltheburn@gmail.com', 'S12', date('now', '-2 days'), 500);
insert into bids values ('B08', 'ibev@gmail.com', 'S03', date('now'), 150);
insert into bids values ('B09', 'rupertd@yahoo.ca', 'S03', date('now', '+1 day'), 300);
insert into bids values ('B10', 'ibev@gmail.com', 'S04', date('now', '-7 days'), 9);
insert into bids values ('B11', 'abanner@ualberta.ca', 'S04', date('now', '-6 days'), 11);
insert into bids values ('B12', 'abanner@ualberta.ca', 'S02', '2020-01-30', 5);
insert into bids values ('B13', 'rupertd@yahoo.ca', 'S12', date('now', '-3 days'), 250);


insert into reviews values ('abanner@ualberta.ca', 'jeansantiago@hotmail.com', 4.6, 'amazing items!', date('now', '-10 days'));
insert into reviews values ('ibev@gmail.com', 'jeansantiago@hotmail.com', 4.3, 'item arrived in perfect condition', date('now'));
insert into reviews values ('rupertd@yahoo.ca', 'jeansantiago@hotmail.com', 5.0, 'incredible!', '2020-02-03');
insert into reviews values ('jeansantiago@hotmail.com', 'abanner@ualberta.ca', 5.0, 'best lister on this site', '2020-01-30');
insert into reviews values ('ibev@gmail.com', 'abanner@ualberta.ca', 4.7, 'no-one better', '2020-01-01');
insert into reviews values ('rupertd@yahoo.ca', 'abanner@ualberta.ca', 4.8, 'amazing', '2019-10-20');
insert into reviews values ('myonlysunshine@outlook.com', 'abanner@ualberta.ca', 5.0, 'best seller you could ask for!', '2019-03-20');
insert into reviews values ('myonlysunshine@outlook.com', 'ibev@gmail.com', 3.0, 'not bad', '2019-04-30');
insert into reviews values ('abanner@ualberta.ca', 'ibev@gmail.com', 4.0, 'servicable', date('now'));
insert into reviews values ('rupertd@yahoo.ca', 'ibev@gmail.com', 3.9, 'okay', date('now'));
insert into reviews values ('myonlysunshine@outlook.com', 'teeltheburn@gmail.com', 4.4, 'yay', '2020-02-03');
insert into reviews values ('rupertd@yahoo.ca', 'teeltheburn@gmail.com', 2.0, 'terrible quality', '2019-01-30');
insert into reviews values ('ibev@gmail.com', 'teeltheburn@gmail.com', 3.0, 'average', '2020-02-04');
insert into reviews values ('myonlysunshine@outlook.com', 'rupertd@yahoo.ca', 4.5, 'good products', '2020-01-29');
insert into reviews values ('ibev@gmail.com', 'rupertd@yahoo.ca', 3.9, 'good', '2020-01-30');
insert into reviews values ('jeansantiago@hotmail.com', 'rupertd@yahoo.ca', 3.3, 'decent', '2020-01-29');
insert into reviews values ('myonlysunshine@outlook.com', 'justhereforfun@live.ca', 1.0, 'terrible quality', '2020-02-03');
insert into reviews values ('teeltheburn@gmail.com', 'justhereforfun@live.ca', 0.5, 'not cool bro', '2020-02-04');
insert into reviews values ('rupertd@yahoo.ca', 'justhereforfun@live.ca', 0.1, 'if i could give zero i would', '2020-02-03');
insert into reviews values ('ibev@gmail.com', 'justhereforfun@live.ca', 0.2, 'im pretty sure it was stolen...', '2020-02-03');


insert into previews values (1, 'X01', 'abanner@ualberta.ca', 4.8, 'I own one, its great with few issues!', date('now', '-1 month'));
insert into previews values (2, 'M01', 'jeansantiago@hotmail.com', 3.0, 'overpriced but not bad!', date('now'));
insert into previews values (3, 'M01', 'teeltheburn@gmail.com', 2.0, 'never any good movies', '2019-03-20');
insert into previews values (4, 'X02', 'myonlysunshine@outlook.com', 4.5, 'great', '2020-01-30');
insert into previews values (5, 'P01', 'myonlysunshine@outlook.com', 3.7, 'not as good as xbox', '2020-02-04');
insert into previews values (6, 'P01', 'teeltheburn@gmail.com', 5.0, 'way better than xbox, so many exclusives!', '2020-02-04');
insert into previews values (7, 'P02', 'justhereforfun@live.ca', 0.1, 'pc is better', '2018-12-12');
insert into previews values (8, 'P01', 'justhereforfun@live.ca', 0.1, 'pc is better', '2018-12-12');
insert into previews values (9, 'P02', 'rupertd@yahoo.ca', 4.5, 'good old console', '2019-12-20');
insert into previews values (10, 'G01', 'ibev@gmail.com', 3.5, 'a little overpriced', '2020-02-02');
insert into previews values (11, 'M03', 'mattress@mattress.com', 4.0, 'great', '2018-02-20');
insert into previews values (12, 'M03', 'mattress@mattress.com', 5.0, 'amazing', date('now', '-2 days'));
