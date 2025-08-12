CREATE TABLE IF NOT EXISTS submissions (
  id serial PRIMARY KEY,
  name varchar(200),
  pan varchar(20),
  aadhaar varchar(20),
  email varchar(200),
  pin varchar(20),
  city varchar(200),
  state varchar(200)
);

INSERT INTO submissions (name, pan, aadhaar, email, pin, city, state) VALUES
('Alice Example','ABCDE1234F','111122223333','alice@example.com','500001','Hyderabad','Telangana'),
('Bob Test','PQRST6789L','999988887777','bob@example.com','110001','New Delhi','Delhi');
