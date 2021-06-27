# Account
## Teacher
``` json
    {
      "person": {
        "first_name": "Nhu",
        "last_name": "Nguyen Thi",
        "gender": "F",
        "date_of_birth": "1995-04-03",
        "address": "178 Tran Hung Dao, Ha Noi",
        "ethnicity": "Kinh",
        "religion" : "None",
        "phone_number": "09224214570"
      },
      "account": {
        "username": "nhunt84",
        "password": "nhu12345678",
        "email": "nhunt@gmail.com"
      }
    }

    {
      "person": {
        "first_name": "Nga",
        "last_name": "Nguyen Thi",
        "gender": "F",
        "date_of_birth": "1993-01-31",
        "address": "19 Nam Dong, Ha Noi",
        "ethnicity": "Kinh",
        "religion" : "None",
        "phone_number": "09904990781"
      },
      "account": {
        "username": "ngant84",
        "password": "nga12345678",
        "email": "ngant@gmail.com"
      }
    }

    {
      "person": {
        "first_name": "Tram",
        "last_name": "Phi Thi",
        "gender": "F",
        "date_of_birth": "1992-09-27",
        "address": "981 Cat Linh, Ha Noi",
        "ethnicity": "Kinh",
        "religion" : "None",
        "phone_number": "09056028783"
      },
      "account": {
        "username": "trampt84",
        "password": "tram12345678",
        "email": "trampt@gmail.com"
      }
    }

```
### Student
``` json
    {
        "person":{
            "first_name": "Hoang",
            "last_name": "Do Minh",
            "gender": "F",
            "date_of_birth": "2000-06-13",
            "address": "180 Phu Luong, Ha Noi",
            "ethnicity": "Kinh",
            "religion" : "None",
            "phone_number": "0947462222"
        }, 
        "classroom_id":17,
        "status":"DH",
        "admission_year":2018,
        "account":{
            "username": "hoangdm13",
            "password": "hoang12345678",
            "email": "hoangdm@gmail.com"
        }
    }
    {
        "person":{
            "first_name": "Long",
            "last_name": "Bui Hoang",
            "gender": "F",
            "date_of_birth": "2000-06-14",
            "address": "179 Phu Luong, Ha Noi",
            "ethnicity": "Kinh",
            "religion" : "None",
            "phone_number": "0928529434"
        }, 
        "classroom_id":18,
        "status":"DH",
        "admission_year":2018,
        "account":{
            "username": "longbh14",
            "password": "long12345678",
            "email": "longbh@gmail.com"
        }
    }
    {
        "person":{
            "first_name": "Hai Long",
            "last_name": "Phan Dinh",
            "gender": "F",
            "date_of_birth": "2000-06-15",
            "address": "178 Phu Luong, Ha Noi",
            "ethnicity": "Kinh",
            "religion" : "None",
            "phone_number": "0982362852"
        }, 
        "classroom_id":18,
        "status":"DH",
        "admission_year":2018,
        "account":{
            "username": "lonhpdh15",
            "password": "hailong12345678",
            "email": "longpdh@gmail.com"
        }
    }
```

```sql
-- Teacher
insert into account(id, username, password, email, is_admin, is_active, join_at)
values (1, "us1", "123456", "us1@gmail.com", false, true, "2021-01-01"),
       (2, "us2", "123456", "us2@gmail.com", false, true, "2021-01-01"),
       (3, "us3", "123456", "us3@gmail.com", false, true, "2021-01-01"),
       (4, "us4", "123456", "us4@gmail.com", false, true, "2021-01-01"),
       (5, "us5", "123456", "us5@gmail.com", false, true, "2021-01-01"),
       (6, "us6", "123456", "us6@gmail.com", false, true, "2021-01-01"),
       (7, "us7", "123456", "us7@gmail.com", false, true, "2021-01-01"),
       (8, "us8", "123456", "us8@gmail.com", false, true, "2021-01-01"),
       (9, "us9", "123456", "us9@gmail.com", false, true, "2021-01-01"),
       (10, "us11", "123456", "us10@gmail.com", false, true, "2021-01-01"),
       (11, "us10", "123456", "us11@gmail.com", false, true, "2021-01-01"),
       (12, "us12", "123456", "us12@gmail.com", false, true, "2021-01-01"),
       (13, "us13", "123456", "us13@gmail.com", false, true, "2021-01-01"),
       (14, "us14", "123456", "us14@gmail.com", false, true, "2021-01-01"),
       (15, "us15", "123456", "us15@gmail.com", false, true, "2021-01-01"),
       (16, "us16", "123456", "us16@gmail.com", false, true, "2021-01-01"),
       (17, "us17", "123456", "us17@gmail.com", false, true, "2021-01-01"),
       (18, "us18", "123456", "us18@gmail.com", false, true, "2021-01-01"),
       (19, "us19", "123456", "us19@gmail.com", false, true, "2021-01-01"),
       (20, "us20", "123456", "us20@gmail.com", false, true, "2021-01-01"),
       (21, "us21", "123456", "us21@gmail.com", false, true, "2021-01-01"),
       (22, "us22", "123456", "us22@gmail.com", false, true, "2021-01-01"),
       (23, "us23", "123456", "us23@gmail.com", false, true, "2021-01-01"),
       (24, "us24", "123456", "us24@gmail.com", false, true, "2021-01-01"),
       (25, "us25", "123456", "us25@gmail.com", false, true, "2021-01-01"),
       (26, "us26", "123456", "us26@gmail.com", false, true, "2021-01-01"),
       (27, "us27", "123456", "us27@gmail.com", false, true, "2021-01-01"),
       (28, "us23", "123456", "us28@gmail.com", false, true, "2021-01-01"),
       (29, "us24", "123456", "us29@gmail.com", false, true, "2021-01-01"),
       (30, "us25", "123456", "us30@gmail.com", false, true, "2021-01-01"),
       (31, "us26", "123456", "us31@gmail.com", false, true, "2021-01-01"),
       (32, "us27", "123456", "us31@gmail.com", false, true, "2021-01-01")

```


# Person Info
```sql

-- Teacher info
insert into person_info(id, first_name, last_name, gender, date_of_birth, address, ethnicity, religion, phone_number)
values (1, 'Ngoc', 'Nguyen Thi', 'F', '1984-04-23', '10 Hai Ba Trung, Ha Noi', 'Kinh', 'None', '09275445385'),
       (2, 'Mai', 'Tran Thi', 'F', '1985-04-10', '52 Ton That Tung, Ha Noi', 'Kinh', 'None', '09996894433'),
       (3, 'Huong', 'Le Thi', 'F', '1986-12-12', '53 Trung Hoa, Ha Noi', 'Kinh', 'None', '09918314975'),
       (4, 'Thao', 'Pham Thi', 'F', '1994-07-11', '25 Yen Hoa, Ha Noi', 'Kinh', 'None', '09515807203'),
       (5, 'Linh', 'Phan Thi', 'F', '1974-08-08', '46 Phuc La, Ha Noi', 'Kinh', 'None', '09646261896'),
       (6, 'Phuong', 'Dang Thi', 'F', '1965-09-07', '489 Hoang Liet, Ha Noi', 'Kinh', 'None', '09620006220'),
       (7, 'Anh', 'Hoang Viet', 'F', '1974-10-06', '383 Thanh Liet, Ha Noi', 'Kinh', 'None', '09964532499'),
       (8, 'Hoa', 'Ngo Thi', 'F', '1989-04-15', '89 Xuan Quan, Ha Noi', 'Kinh', 'None', '09589309467'),
       (9, 'Ha', 'Do Thi', 'F', '1995-03-23', '268 La Khe, Ha Noi', 'Kinh', 'None', '09396021192'),
       (10, 'Chi', 'Nguyen Thi', 'F', '1984-04-30', '157 Quang Trung, Ha Noi', 'Kinh', 'None', '09623916428'),
       (11, 'Nhung', 'Nguyen Thi', 'F', '1989-04-28', '278 Hai Ba Trung, Ha Noi', 'Kinh', 'None', '09437383581'),
       (12, 'Uyen', 'Phi Thi', 'F', '1989-04-29', '289 Phu Thuong, Ha Noi', 'Kinh', 'None', '09520010887'),
       (13, 'Tam', 'Nguyen Thi', 'F', '1954-04-23', '21 Mai Lam, Ha Noi', 'Kinh', 'None', '09397722080'),
       (14, 'Dan', 'Tran Thi', 'F', '1965-04-10', '67 Dong Ngac, Ha Noi', 'Kinh', 'None', '09663209009'),
       (15, 'Trang', 'Le Thi', 'F', '1946-12-12', '238 Lien Mac, Ha Noi', 'Kinh', 'None', '09125699948'),
       (16, 'Yen', 'Pham Thi', 'F', '1957-07-11', '135 Dong Anh, Ha Noi', 'Kinh', 'None', '09103338193'),
       (17, 'Lan', 'Phan Thi', 'F', '1956-08-08', '589 Thuy Lam, Ha Noi', 'Kinh', 'None', '09739723036'),
       (18, 'Ngan', 'Dang Thi', 'F', '1965-09-07', '147 Bac Viet, Ha Noi', 'Kinh', 'None', '09430301754'),
       (19, 'Chau', 'Hoang Viet', 'F', '1978-10-06', '178 Nam Hong, Ha Noi', 'Kinh', 'None', '09790677179'),
       (20, 'Chi', 'Ngo Thi', 'F', '1985-04-15', '147 Tien Phong, Ha Noi', 'Kinh', 'None', '09183101489'),
       (21, 'Thuy', 'Do Thi', 'F', '1958-03-23', '148 Van Noi, Ha Noi', 'Kinh', 'None', '09853010227'),
       (22, 'Thu', 'Nguyen Thi', 'F', '1998-04-30', '17 Vong La, Ha Noi', 'Kinh', 'None', '09678883267'),
       (23, 'Vy', 'Nguyen Thi', 'F', '1989-04-28', '167 Thuong Cat, Ha Noi', 'Kinh', 'None', '09483703004'),
       (24, 'Hue', 'Phi Thi', 'F', '1948-04-29', '481 Duong Lieu, Ha Noi', 'Kinh', 'None', '09850731524'),
       (25, 'Hong', 'Tran Thi', 'F', '1986-01-10', '16 Tho Xuan, Ha Noi', 'Kinh', 'None', '09678960885'),
       (26, 'Hien', 'Le Thi', 'F', '1979-03-12', '72 Dan Phuong, Ha Noi', 'Kinh', 'None', '09305856601'),
       (27, 'THao', 'Pham Thi', 'F', '1978-07-24', '124 Hiep Thuan, Ha Noi', 'Kinh', 'None', '09345941674'),
       (28, 'An', 'Phan Thi', 'F', '1974-12-25', '358 Canh Nau, Ha Noi', 'Kinh', 'None', '09712687303'),
       (29, 'Lan', 'Dang Thi', 'F', '1990-10-17', '123 Huong Ngai, Ha Noi', 'Kinh', 'None', '09744831734'),
       (30, 'Thanh', 'Hoang Viet', 'F', '1990-10-14', '14 Sai Son, Ha Noi', 'Kinh', 'None', '09336397388'),
       (31, 'My', 'Ngo Thi', 'F', '1979-06-15', '148 Van Phuc, Ha Noi', 'Kinh', 'None', '09922951999'),
       (32, 'Nhi', 'Do Thi', 'F', '1986-03-08', '184 Phu Luong, Ha Noi', 'Kinh', 'None', '09947467251')

```

# Teacher
```sql
  insert into teacher(account_id, person_id)
  values (1, 1),
         (2, 2),
         (3, 3),
         (4, 4),
         (5, 5),
         (6, 6),
         (7, 7),
         (8, 8),
         (9, 9),
         (10, 10),
         (12, 12),
         (13, 13),
         (14, 14),
         (15, 15),
         (16, 16),
         (17, 17),
         (18, 18),
         (19, 19),
         (20, 20),
         (21, 21),
         (22, 22),
         (23, 23),
         (24, 24),
         (25, 25),
         (26, 26),
         (27, 27),
         (28, 28),
         (29, 29),
         (30, 30),
         (31, 31),
         (32, 32),

```

# Classroom
```sql
insert into classrom(class_name, location)
values ('10A', 'B102', 1),
       ('10B', 'B103', 2),
       ('10C', 'B104', 3),
       ('10D', 'B105', 4),
       ('10E', 'B106', 5),
       ('10H', 'B107', 6),
       ('10G', 'B108', 7),
       ('10H', 'B109', 8),
       ('11A', 'B202', 9),
       ('11B', 'B203', 10),
       ('11C', 'B204', 11),
       ('11D', 'B205', 12),
       ('11E', 'B206', 13),
       ('11H', 'B207', 14),
       ('11G', 'B208', 15),
       ('11H', 'B209', 16),
       ('12A', 'B302', 17),
       ('12B', 'B303', 18),
       ('12C', 'B304', 19),
       ('12D', 'B305', 20),
       ('12E', 'B306', 21),
       ('12H', 'B307', 22),
       ('12G', 'B308', 23),
       ('12H', 'B309', 24);
```

# Course
```sql
insert into course(course_name, group_course)
values ('Toan', 'Sc'),
       ('Ngu van', 'So'),
       ('Ngoai ngu', 'So'),
       ('Giao duc con dan', 'So'),
       ('Dia ly', 'Sc'),
       ('Hoa hoc', 'Sc'),
       ('Vat ly', 'Sc'),
       ('Sinh hoc', 'Sc'),
       ('Cong nghe', 'Sc'),
       ('Tin hoc', 'Sc'),
       ('Giao duc the chat', 'Ph'),
       ('Giao duc quoc phong', 'Ph');
```

# Achievement
```sql
insert into achievement(achievement_name)
values ('Hoc sinh gioi 2021'),
       ('Hoc sinh tien tien 2021'),
       ('Hoc sinh gioi Toan thanh pho 2021'),
       ('Hoc sinh gioi Ngu van thanh pho 2021'),
       ('Hoc sinh gioi Vat ly thanh pho 2021'),
       ('Hoc sinh gioi Hoa hoc thanh pho 2021'),
       ('Hoc sinh gioi Ngoai ngu thanh pho 2021'),
       ('Giao vien xuat sac 2021'),
       ('Giao vien gioi thanh pho 2021'),
       ('Lop xuat sac 2021')

```

# Device
```sql
insert into device(device_name, status, amount, price)
values ('Dai cat set', 'O', 10, 200000),
       ('Dai Casio', 'N', 20, 500000),
       ('Dieu hoa Tosiba', 'N', 30, 5000000),
       ('May chieu', 'N', 30, 10000000),
       ('Loa', 'N', 10, 300000),
       ('Mic', 'N', 24, 200000)
```
# Conduct
```sql
insert into conduct(score, semester, school_year, student_id) 
values 
       ('K', 1, 2018, 1),
       ('T', 2, 2018, 1),
       ('T', 1, 2019 , 1),
       ('T', 2, 2019, 1),
       ('T', 1, 2020, 1),

       ('T', 1, 2018, 2),
       ('T', 2, 2018, 2),
       ('T', 1, 2019, 2),
       ('T', 2, 2019, 2),
       ('T', 1, 2020, 2),

       ('K', 1, 2018, 3),
       ('T', 2, 2018, 3),
       ('K', 1, 2019, 3),
       ('T', 2, 2019, 3),
       ('T', 1, 2020, 3),

insert into conduct(semester, school_year, student_id) 
values 
       (2, 2021, 1),
       (2, 2021, 2),
       (2, 2021, 3),
```
# Grade
```sql
insert into grade(student_id, course_id, school_year, semester, quiz1, quiz2, quiz3, test, mid_term_test, final_test, start_update)
values 
      (1, 1, 2020, 1, 10, 9, 9, 8.5, 7.5, 9, '2020-12-28'),
      (1, 2, 2020, 1, 8, 9, 7, 8.5, 7, 9, '2020-12-28'),
      (1, 3, 2020, 1, 10, 7, 9, 8, 7.5, 9.5, '2020-12-28'),
      (1, 4, 2020, 1, 8.5, 9.5, 9.5, 8, 7.5, 8, '2020-12-28'),
      (1, 5, 2020, 1, 6, 7.5, 7, 8, 7.5, 7.5, '2020-12-28'),
      (1, 6, 2020, 1, 8, 8, 6, 8.5, 7.5, 7, '2020-12-28'),
      (1, 7, 2020, 1, 9, 9, 9, 8.5, 7.5, 7, '2020-12-28'),
      (1, 8, 2020, 1, 7, 9, 9, 8.5, 7.5, 8, '2020-12-28'),
      (1, 9, 2020, 1, 7, 9, 9, 8.5, 7.5, 8.5, '2020-12-28'),
      (1, 10, 2020, 1, 8, 9, 7, 8.5, 7.5, 9, '2020-12-28'),
      (1, 11, 2020, 1, 10, 9, 8, 8.5, 7.5, 10, '2020-12-28'),
      (1, 12, 2020, 1, 7, 5, 6.5, 8.5, 7.5, 6, '2020-12-28'),

      (2, 1, 2020, 1, 8.5, 9, 7.5, 8.5, 7.5, 6, '2020-12-28'),
      (2, 2, 2020, 1, 8, 9, 7.5, 7.5, 8, 10, '2020-12-28'),
      (2, 3, 2020, 1, 10, 7.5, 9.5, 8, 7.5, 9.5, '2020-12-28'),
      (2, 4, 2020, 1, 8, 9.5, 8, 8, 7.5, 8, '2020-12-28'),
      (2, 5, 2020, 1, 6.5, 7, 7, 8, 7.5, 9, '2020-12-28'),
      (2, 6, 2020, 1, 8, 8, 10, 8.5, 5, 7.5, '2020-12-28'),
      (2, 7, 2020, 1, 9, 9, 10, 8.5, 10, 9, '2020-12-28'),
      (2, 8, 2020, 1, 7, 9.5, 9, 8, 7.5, 8.5, '2020-12-28'),
      (2, 9, 2020, 1, 7.5, 9, 9.5, 8.5, 7, 8.5, '2020-12-28'),
      (2, 10, 2020, 1, 8.5, 9, 7.5, 8.5, 7, 9.5, '2020-12-28'),
      (2, 11, 2020, 1, 10, 9, 8.5, 8.5, 7, 10, '2020-12-28'),
      (2, 12, 2020, 1, 7, 10, 6.5, 10, 9, 6.5, '2020-12-28'),

      (3, 1, 2020, 1, 8, 9, 8, 7, 7.5, 9.5, '2020-12-28'),
      (3, 2, 2020, 1, 8.5, 9, 8, 8, 8, 9.5, '2020-12-28'),
      (3, 3, 2020, 1, 10, 10, 9, 8, 10, 9.5, '2020-12-28'),
      (3, 4, 2020, 1, 7.5, 9, 9, 8, 7, 8, '2020-12-28'),
      (3, 5, 2020, 1, 8, 6.5, 7, 8, 6.5, 8.5, '2020-12-28'),
      (3, 6, 2020, 1, 9, 8, 6.5, 8.5, 8.5, 7.5, '2020-12-28'),
      (3, 7, 2020, 1, 9.5, 9, 9, 8.5, 7.5, 7.5, '2020-12-28'),
      (3, 8, 2020, 1, 7, 9, 9, 8.5, 7.5, 8, '2020-12-28'),
      (3, 9, 2020, 1, 7.5, 8, 9, 8, 7.5, 8.5, '2020-12-28'),
      (3, 10, 2020, 1, 8.5, 9, 7.5, 8.5, 7.5, 9, '2020-12-28'),
      (3, 11, 2020, 1, 10, 9, 10, 8.5, 6.5, 10, '2020-12-28'),
      (3, 12, 2020, 1, 7.5, 8, 7.5, 8.5, 8.5, 10, '2020-12-28'),

insert into grade(student_id, course_id, school_year, semester, start_update)
values 
      (1, 1, 2020, 2, '2021-06-28'),
      (1, 2, 2020, 2, '2021-06-28'),
      (1, 3, 2020, 2, '2021-06-28'),
      (1, 4, 2020, 2, '2021-06-28'),
      (1, 5, 2020, 2, '2021-06-28'),
      (1, 6, 2020, 2, '2021-06-28'),
      (1, 7, 2020, 2, '2021-06-28'),
      (1, 8, 2020, 2, '2021-06-28'),
      (1, 9, 2020, 2, '2021-06-28'),
      (1, 10, 2020, 2, '2021-06-28'),
      (1, 11, 2020, 2, '2021-06-28'),
      (1, 12, 2020, 2, '2021-06-28'),

      (2, 1, 2020, 2, '2021-06-28'),
      (2, 2, 2020, 2, '2021-06-28'),
      (2, 3, 2020, 2, '2021-06-28'),
      (2, 4, 2020, 2, '2021-06-28'),
      (2, 5, 2020, 2, '2021-06-28'),
      (2, 6, 2020, 2, '2021-06-28'),
      (2, 7, 2020, 2, '2021-06-28'),
      (2, 8, 2020, 2, '2021-06-28'),
      (2, 9, 2020, 2, '2021-06-28'),
      (2, 10, 2020, 2, '2021-06-28'),
      (2, 11, 2020, 2, '2021-06-28'),
      (2, 12, 2020, 2, '2021-06-28'),

      (3, 1, 2020, 2, '2021-06-28'),
      (3, 2, 2020, 2, '2021-06-28'),
      (3, 3, 2020, 2, '2021-06-28'),
      (3, 4, 2020, 2, '2021-06-28'),
      (3, 5, 2020, 2, '2021-06-28'),
      (3, 6, 2020, 2, '2021-06-28'),
      (3, 7, 2020, 2, '2021-06-28'),
      (3, 8, 2020, 2, '2021-06-28'),
      (3, 9, 2020, 2, '2021-06-28'),
      (3, 10, 2020, 2, '2021-06-28'),
      (3, 11, 2020, 2, '2021-06-28'),
      (3, 12, 2020, 2, '2021-06-28'),
```
