create database if not exists aegis;

use aegis;

create table if not exists dongleData (
                                     id         integer auto_increment primary key,
                                     outlet_name varchar(255) not null,
                                     amps  varchar(255),
                                     temp float,
                                     measured_at timestamp not null default current_timestamp
);

create table if not exists commands (
                                        id         integer auto_increment primary key,
                                        to_ID  varchar(255) not null,
                                        from_ID varchar(255) not null,
                                        command varchar(255) not null,
                                        created_at timestamp not null default current_timestamp
);
