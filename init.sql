create table students(
student_id       serial primary key,
full_name        varchar(255) not null UNIQUE
);

create table data_about_students
(
record_id        serial primary key,
estimation       smallint not null CHECK (estimation >= 2 AND estimation <= 5),
student_id       int not null,
constraint key_users foreign key(student_id) references students(student_id)
)