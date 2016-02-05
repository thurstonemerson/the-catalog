-- Create database for the catalog project.
-- \i catalog.sql 
-- need appropriate permissions - sudo su postgres

create user catalog with password 'YLrvke37pa9JR5x7';
create database thecatalog owner catalog;

