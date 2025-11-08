create table department(
	DeptName varchar(50),
	Building varchar(40) not null,
	Budget numeric(11, 2) not null check (budget > 0),
	primary key(deptname)
);

create table instructor(
	id varchar(7),
	name varchar(50) not null,
	Salary numeric(8, 2) not null,
	deptName varchar(50) not null,
	primary key(id),
	foreign key(deptname) references department
);

create table student(
	ID varchar(7),
	Name varchar(50) not null,
	DOB date not null,
	deptName varchar(50) not null,
	primary key(id),
	foreign key(deptname) references department on delete set null
);

create table Mentoring(
	StudentID varchar(7),
	InstructorID varchar(7),
	primary key(studentid, instructorid), -- composite primary key
	foreign key(studentid) references student,
	foreign key(instructorid) references instructor
);

create table Course(
	CourseCode varchar(8),
	Title varchar(50) not null,
	Credits integer not null check (credits > 0),
	deptname varchar(50) not null,
	primary key(coursecode),
	foreign key(deptname) references department on delete set null
);

create table Prerequisites(
	CourseCode varchar(8),
	PreqID varchar(8),
	primary key(coursecode, preqid),
	foreign key(coursecode) references course,
	foreign key(preqid) references course
);

create table Classroom(
	Building varchar(40),
	RoomNumber varchar(5),
	Capacity integer not null,
	primary key(building, roomnumber)
);

create table Section(
	CourseCode varchar(8),
	sectionid varchar(3),
	Semester varchar(10) check (semester in ('Fall', 'Winter', 'Spring', 'Summer')),
	Year integer, -- alias (int)
	Building varchar(40) not null,
	RoomNumber varchar(5) not null,
	primary key(coursecode, sectionid, semester, year), -- composite primary key
	foreign key(coursecode) references course on delete cascade,
	foreign key(building, roomnumber) references classroom on delete set null
);

create table Teaches(
	CourseCode varchar(8),
	SectionID varchar(3),
	Semester varchar(10),
	Year integer,
	InstructorID varchar(7),
	primary key(coursecode, sectionid, semester, year, instructorid),
	foreign key(coursecode, sectionid, semester, year) references section on delete cascade,
	foreign key(instructorid) references instructor on delete cascade
);

create table takes(
	CourseCode varchar(8),
	SectionID varchar(3),
	Semester varchar(10),
	Year integer,
	studentID varchar(7),
	grade char(1),
	primary key(coursecode, sectionid, semester, year, studentid),
	foreign key(coursecode, sectionid, semester, year) references section on delete cascade,
	foreign key(studentid) references student on delete cascade
)