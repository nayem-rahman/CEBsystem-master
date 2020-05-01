SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS card_info;
DROP TABLE IF EXISTS promotion;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS showroom;
DROP TABLE IF EXISTS showing;
DROP TABLE IF EXISTS seat;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS price;
-- SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE IF NOT EXISTS user (
	user_id 		INT 			AUTO_INCREMENT PRIMARY KEY, 
    first_name		VARCHAR(30)		NOT NULL,
    last_name		VARCHAR(30)		NOT NULL,
    email	        VARCHAR(30) 	NOT NULL,
    password        VARCHAR(500)     NOT NULL, 
    status  		INT	            NOT NULL,
    sub_to_promo	BOOL
);

CREATE TABLE IF NOT EXISTS card_info (
    payment_id  INT 			AUTO_INCREMENT PRIMARY KEY,
    user_id     INT             NOT NULL,
    card_num 	VARCHAR(300)    NOT NULL,
    cvv			VARCHAR(4)      NOT NULL,
    exp_month	VARCHAR(20)     NOT NULL,
    exp_year	VARCHAR(4)      NOT NULL,
    full_name   VARCHAR(60)		NOT NULL,
    name_card   VARCHAR(60)		NOT NULL,
	address     VARCHAR(50)		NOT NULL,
    city		VARCHAR(30)		NOT NULL,
    state		VARCHAR(30)		NOT NULL,
    zip			VARCHAR(10) 	NOT NULL,
    CONSTRAINT user_fk FOREIGN KEY (user_id)
    REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS promotion (
    promotion_id  	INT 			AUTO_INCREMENT PRIMARY KEY,
    promo_code 		VARCHAR(10)		NOT NULL,
    start_date		DATE			NOT NULL,
    end_date		DATE			NOT NULL,
    discount_pct	INT				NOT NULL
);

CREATE TABLE IF NOT EXISTS movie (
    movie_id  		INT 			AUTO_INCREMENT PRIMARY KEY,
    movie_name 		VARCHAR(30)		NOT NULL,
	genre 			VARCHAR(30)		NOT NULL,
    rating 			VARCHAR(5)		NOT NULL,
    description		TEXT			NOT NULL,
    image_url		TEXT			NOT NULL,
    trailer_link	TEXT			NOT NULL,
    run_time		VARCHAR(30)		NOT NULL,
    stars           TEXT            NOT NULL,
    director        TEXT            NOT NULL,
    producer        TEXT            NOT NULL
);

CREATE TABLE IF NOT EXISTS showroom (
    showroom_id  	INT 	AUTO_INCREMENT PRIMARY KEY,
    room_num 		INT		NOT NULL,
    num_seats		INT		NOT	NULL
);

CREATE TABLE IF NOT EXISTS price (
	price_id INT AUTO_INCREMENT PRIMARY KEY,
    type 		 VARCHAR(30)	NOT NULL,
	ticket_price DECIMAL(4,2)	NOT NULL
);

CREATE TABLE IF NOT EXISTS showing (
    show_id  		INT 			AUTO_INCREMENT PRIMARY KEY,
    show_time		TIME			NOT NULL,
    movie_id 		INT				NOT NULL,
    showroom_id		INT				NOT NULL,
    start_date      DATE            NOT NULL,
    end_date        DATE            NOT NULL,
    CONSTRAINT movie_fk FOREIGN KEY (movie_id)
    REFERENCES movie(movie_id),
	CONSTRAINT showroom_fk FOREIGN KEY (showroom_id)
    REFERENCES showroom(showroom_id)
);

CREATE TABLE IF NOT EXISTS seat (
    seat_id  	INT 	AUTO_INCREMENT PRIMARY KEY,
    seat_num 	VARCHAR(10)		NOT NULL,
	show_id		INT		NOT NULL,
	CONSTRAINT show_seat_fk FOREIGN KEY (show_id)
    REFERENCES showing(show_id)
);


CREATE TABLE IF NOT EXISTS booking (
    booking_id     INT 	AUTO_INCREMENT PRIMARY KEY,
    user_id        INT  NOT NULL,
    card_id		   INT  NOT NULL,
    show_id        INT  NOT NULL,
    tickets        VARCHAR(100) NOT NULL,
    total_price    FLOAT NOT NULL,
    purchase_date   DATE NOT NULL,
    CONSTRAINT user_book_fk FOREIGN KEY (user_id)
    REFERENCES user(user_id),
    CONSTRAINT card_fk FOREIGN KEY (card_id)
    REFERENCES card_info(payment_id),
    CONSTRAINT show_book_fk FOREIGN KEY (show_id)
    REFERENCES showing(show_id)
);

CREATE TABLE IF NOT EXISTS ticket (
    ticket_id  INT	AUTO_INCREMENT PRIMARY KEY,
    booking_id    INT  NOT NULL,
    ticket_type INT NOT NULL,
    seat_id INT NOT NULL,
    price_id INT NOT NULL,
    CONSTRAINT booking_ticket_fk FOREIGN KEY (booking_id)
    REFERENCES booking(booking_id),
    CONSTRAINT seat_ticket_fk FOREIGN KEY (seat_id)
    REFERENCES seat(seat_id),
    CONSTRAINT price_fk FOREIGN KEY (price_id)
    REFERENCES price(price_id)
);



/* FILL WITH EXAMPLE DATA */

-- users
INSERT INTO `user` (`first_name`,`last_name`,`email`,`password`,`status`, `sub_to_promo`) VALUES ("test","account","test@gmail.com","gAAAAABduhMLrV-GBJfQ_9JKM6MaHmU4p4feBsSXCLie9knM4y15IFKJrYT4HGfuMgxETgvTu8WYLNvJ2586PUZ8d4vYFca8lQ==",1,0);
INSERT INTO `user` (`first_name`,`last_name`,`email`,`password`,`status`) VALUES ("admin","account","admin@gmail.com","gAAAAABduhMLrV-GBJfQ_9JKM6MaHmU4p4feBsSXCLie9knM4y15IFKJrYT4HGfuMgxETgvTu8WYLNvJ2586PUZ8d4vYFca8lQ==",2);

-- payment
-- INSERT INTO `card_info` (`user_id`,`card_num`,`cvv`,`expiration`,`first_name`,`last_name`,`street`,`city`,`state`,`zip`, `phone`) VALUES (2,"0000-0000-0000-0000","123","2022-01-01","John","Customer","1234 Main Street","Nashville","TN","12345","111-222-3333");

-- promotion
INSERT INTO `promotion` (`promo_code`,`start_date`,`end_date`,`discount_pct`) VALUES ("GREATDEAL","2019-11-01","2019-11-20",1);

-- movie
INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Joker",
                                                                                                                "Thriller",
                                                                                                                "R",
                                                                                                                "mentally-troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime.",
                                                                                                                "https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SY1000_CR0,0,674,1000_AL_.jpg","https://www.youtube.com/watch?v=zAGVQLHvwOY",
                                                                                                                "2h 2m",
                                                                                                                "Joaquin Phoenix, Robert De Niro, Zazie Beetz",
                                                                                                                "Todd Phillips",
                                                                                                                "Todd Phillips");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("It Chapter Two",
                                                                                                                "Horror",
                                                                                                                "R",
                                                                                                                "Twenty-seven years after their first encounter with the terrifying Pennywise, the Losers Club have grown up and moved away, until a devastating phone call brings them back.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/216994/itchapter2%20-%20Final%20Art.jpg",
                                                                                                                "https://www.youtube.com/watch?v=xhJ5P7Up3jA",
                                                                                                                "2h 49m",
                                                                                                                "Jessica Chastain, James McAvoy, Bill Hader",
                                                                                                                "Andy Muschietti",
                                                                                                                "Barbara Muschietti");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("The Lion King", 
                                                                                                                "Drama", 
                                                                                                                "PG", 
                                                                                                                "After the murder of his father, a young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/215915/TheLionKing5c736ad86cb97.jpg",
                                                                                                                "https://www.youtube.com/watch?v=7TavVZMewpY",
                                                                                                                "2h 49m",
                                                                                                                "Donald Glover, Beyoncé, Seth Rogen",
                                                                                                                "Jon Favreau",
                                                                                                                "Jon Favreau");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Spiderman: Far From Home",
                                                                                                                "Action",
                                                                                                                "PG-13",
                                                                                                                "Following the events of Avengers: Endgame (2019), Spider-Man must step up to take on new threats in a world that has changed forever.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/216033/spider-man-far-from-home-SFFH_OnLine_1SHT_6072x9000_TSR_04_rgb.jpg",
                                                                                                                "https://www.youtube.com/watch?v=Nt9L1jCKGnE",
                                                                                                                "2h 9m",
                                                                                                                "Tom Holland, Samuel L. Jackson, Jake Gyllenhaal",
                                                                                                                "Jon Watts",
                                                                                                                "Kevin Feige");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Ad Astra",
                                                                                                                "Action",
                                                                                                                "PG-13",
                                                                                                                "Astronaut Roy McBride undertakes a mission across an unforgiving solar system to uncover the truth about his missing father and his doomed expedition that now, 30 years later, threatens the universe.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/219166/AdAstra_VerC_Poster_R2_sRGB.JPG",
                                                                                                                "https://www.youtube.com/watch?v=BsCNKuB93BA",
                                                                                                                "2h 2m",
                                                                                                                "Brad Pitt, Tommy Lee Jones, Ruth Negga",
                                                                                                                "James Gray",
                                                                                                                "Brad Pitt");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Good Boys (2019)",
                                                                                                                "Comedy",
                                                                                                                "R",
                                                                                                                "Three 6th grade boys ditch school and embark on an epic journey while carrying accidentally stolen drugs, being hunted by teenage girls, and trying to make their way home in time for a long-awaited party.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/217779/GoodBoys2019.jpg",
                                                                                                                "https://www.youtube.com/watch?v=zPXqwAGmX04",
                                                                                                                "1h 35m",
                                                                                                                "Jacob Tremblay, Keith L. Williams, Brady Noon",
                                                                                                                "Gene Stupnitsky",
                                                                                                                "Lee Eisenberg");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Hustlers",
                                                                                                                "Comedy",
                                                                                                                "R",
                                                                                                                "Inspired by the viral New York Magazine article, Hustlers follows a crew of savvy former strip club employees who band together to turn the tables on their Wall Street clients.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/218764/HUSTLERS_27x40_sRGB.jpg",
                                                                                                                "https://www.youtube.com/watch?v=lDv-TwjQ_o4",
                                                                                                                "1h 50m",
                                                                                                                "Constance Wu, Jennifer Lopez, Julia Stiles",
                                                                                                                "Lorene Scafaria",
                                                                                                                "Jessica Elbaum");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Terminator: Dark Fate",
                                                                                                                "Action",
                                                                                                                "R",
                                                                                                                "Sarah Connor and a hybrid cyborg human must protect a young girl from a newly modified liquid Terminator from the future.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/masterrepository/Fandango/218973/TerminatorDarkFate2019.jpg",
                                                                                                                "https://www.youtube.com/watch?v=oxy8udgWRmo",
                                                                                                                "2h 8m",
                                                                                                                "Linda Hamilton, Arnold Schwarzenegger, Mackenzie Davis",
                                                                                                                "Tim Miller",
                                                                                                                "James Cameron");
                                                                                                                
INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Last Christmas (2019)",
                                                                                                                "Comedy",
                                                                                                                "PG-13",
                                                                                                                "Kate is a young woman subscribed to bad decisions. Her last date with disaster? That of having accepted to work as Santa's elf for a department store. However, she meets Tom there. Her life takes a new turn. For Kate, it seems too good to be true.",
                                                                                                                "https://images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/masterrepository/Fandango/219795/LastChristmas2019.jpg",
                                                                                                                "https://www.youtube.com/watch?v=z9CEIcmWmtA",
                                                                                                                "1h 42m",
                                                                                                                "Madison Ingoldsby, Emma Thompson, Boris Isakovic",
                                                                                                                "Paul Feig",
                                                                                                                "Erik Baiers");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Doctor Sleep",
                                                                                                                "Horror",
                                                                                                                "R",
                                                                                                                "Years following the events of The Shining,a now-adult Dan Torrance must protect a young girl with similar powers from a cult known as The True Knot, who prey on children with powers to remain immortal.",
                                                                                                                "https://regalcdn.azureedge.net/DoctorSleep/HO00009866/TV_SmallPosterImage/20191009-124901292.jpg",
                                                                                                                "https://www.youtube.com/watch?v=eFkmiAw5Av8",
                                                                                                                "2h 32m",
                                                                                                                "Ewan McGregor, Rebecca Ferguson, Kyliegh Curran",
                                                                                                                "Mike Flanagan",
                                                                                                                "Trevor Macy");

INSERT INTO `movie` (`movie_name`,`genre`,`rating`,`description`,`image_url`,`trailer_link`,`run_time`, `stars`,`director`,`producer`) VALUES ("Midway",
                                                                                                                "Action",
                                                                                                                "PG-13",
                                                                                                                "The story of the Battle of Midway, told by the leaders and the sailors who fought it.",
                                                                                                                "https://regalcdn.azureedge.net/Midway/HO00009733/TV_SmallPosterImage/20191030-125407466.jpg",
                                                                                                                "https://www.youtube.com/watch?v=l9laReRAYFk",
                                                                                                                "2h 18m",
                                                                                                                "Ed Skrein, Patrick Wilson, Woody Harrelson",
                                                                                                                "Roland Emmerich",
                                                                                                                "Roland Emmerich");
-- showroom
INSERT INTO `showroom` (`room_num`,`num_seats`) VALUES (1,100);
INSERT INTO `showroom` (`room_num`,`num_seats`) VALUES (2,100);
INSERT INTO `showroom` (`room_num`,`num_seats`) VALUES (3,50);
INSERT INTO `showroom` (`room_num`,`num_seats`) VALUES (4,50);

-- price
INSERT INTO `price` (`type`,`ticket_price`) VALUES ("child",6.50);
INSERT INTO `price` (`type`,`ticket_price`) VALUES ("adult",8.00);
INSERT INTO `price` (`type`,`ticket_price`) VALUES ("senior",6.50);

-- showing
INSERT INTO `showing` (`show_time`,`movie_id`,`showroom_id`, `start_date`, `end_date`) VALUES ("11:15:00",1,1,"2019-11-01","2019-12-20");
INSERT INTO `showing` (`show_time`,`movie_id`,`showroom_id`, `start_date`, `end_date`) VALUES ("15:30:00",1,2,"2019-11-01","2019-12-20");
INSERT INTO `showing` (`show_time`,`movie_id`,`showroom_id`, `start_date`, `end_date`) VALUES ("12:30:00",2,2,"2019-11-01","2019-12-20");
INSERT INTO `showing` (`show_time`,`movie_id`,`showroom_id`, `start_date`, `end_date`) VALUES ("09:10:00",3,3,"2019-11-01","2019-12-20");
INSERT INTO `showing` (`show_time`,`movie_id`,`showroom_id`, `start_date`, `end_date`) VALUES ("09:45:00",4,4,"2019-11-01","2019-12-20");
INSERT INTO `showing` (`show_time`,`movie_id`,`showroom_id`, `start_date`, `end_date`) VALUES ("13:10:00",5,4,"2019-11-01","2019-12-20");

-- seats
-- INSERT INTO `seat` (`seat_num`,`reserved`, `show_id`) VALUES (1,FALSE,1);
-- INSERT INTO `seat` (`seat_num`,`reserved`, `show_id`) VALUES (2,FALSE,1);
-- INSERT INTO `seat` (`seat_num`,`reserved`, `show_id`) VALUES (3,FALSE,1);
-- INSERT INTO `seat` (`seat_num`,`reserved`, `show_id`) VALUES (4,FALSE,1);
-- INSERT INTO `seat` (`seat_num`,`reserved`, `show_id`) VALUES (5,FALSE,1);

-- booking
-- INSERT INTO `booking` (`user_id`, `card_id`,`show_id`,`complete`) VALUES (2,1,1,FALSE);

-- ticket
-- INSERT INTO `ticket` (`booking_id`,`ticket_type`,`seat_id`,`price_id`) VALUES (1,2,1,2);
-- INSERT INTO `ticket` (`booking_id`,`ticket_type`,`seat_id`,`price_id`) VALUES (1,2,1,1);