
CREATE DATABASE IF NOT EXISTS thesis;

CREATE USER IF NOT EXISTS thesis_user IDENTIFIED WITH mysql_native_password BY 'thesis_password_12345';

GRANT ALL PRIVILEGES ON *.* TO thesis_user;
