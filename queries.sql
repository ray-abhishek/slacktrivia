INSERT INTO category(name,flag) VALUES ("Television",true),("Sports",true),("History",true);



INSERT INTO question(question,option1,option2,option3,option4,answer) VALUES ("Who played Chandler's father on Friends?","KATHLEEN TURNER","NATHAN LANE","MICHAEL DOUGLAS","ELLIOT GOULD","KATHLEEN TURNER"),("Every episode of Seinfeld contains an image or reference to what superhero?","BATMAN","SUPERMAN","SPIDERMAN","PLASTIC MAN","SUPERMAN"),("Who was the youngest person to host Saturday Night Live?","MACAULAY CULKIN","FRED SAVAGE","DREW BARRYMORE","MILEY CYRUS","DREW BARRYMORE"),("What was the shortest war in human history?","ENGLAND AND ZANZIBAR","INDIA AND CHINA","USA AND CANADA","NORTH KOREA AND SOUTH KOREA","ENGLAND AND ZANZIBAR"),("How many years did the 100 years war last?","100","200","50","116","116"),("In which year was John F. Kennedy assassinated?","1978","1947","1963","1945","1963"),("What club did retired footballer Zinedine Zidane play for during the 1997-98 season?","REAL MADRID","ARSENAL","JUVENTUS","MOHUN BAGAN","JUVENTUS"),("How many NBA championships did Michael Jordan win with the Chicago Bulls?","15","24","9","6","6"),("Which boxer inflicted Muhammad Ali’s first defeat in professional boxing?","George Foreman","Joe Frazier","Mike Tyson","Floyd Mayweather","Joe Frazier");


INSERT INTO question_category(question_id,category_id) VALUES(1,1),(2,1),(3,1),(4,3),(5,3),(6,3),(7,2),(8,2),(9,2);

