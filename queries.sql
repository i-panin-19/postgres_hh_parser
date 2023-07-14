-- SQL-команды для создания таблиц

CREATE DATABASE hh_vacancies;

CREATE TABLE employers
(
    employer_id int PRIMARY KEY,
    employer_name varchar(100) NOT NULL,
    open_vacancies smallint NOT NULL,
    employer_url varchar(100) NOT NULL
);

CREATE TABLE vacancies
(
    vacancy_id serial PRIMARY KEY,
    employer_id int REFERENCES employers(employer_id) NOT NULL,
    vacancy_name varchar(100) NOT NULL,
    salary_from int NOT NULL,
    salary_to int NOT NULL,
    salary_currency varchar(5),
    vacancy_notes text NOT NULL,
    vacancy_url varchar(100) NOT NULL
);

SELECT * FROM employers;

SELECT * FROM vacancies;

TRUNCATE vacancies, employers RESTART IDENTITY;

DROP DATABASE hh_vacancies;

