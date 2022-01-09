--example of db initiatilizaton
CREATE USER thesis IDENTIFIED BY 'thesis_password_12345';
-- for tests
GRANT ALL PRIVILEGES ON *.* TO thesis;

CREATE DATABASE thesis;