create database webapp;
use webapp;

#create mission
create table mission(
	mission_id int(9) not null primary key auto_increment,
	mission_name varchar(100) not null,
	accomplish int(3),
	remark varchar(200)
)engine=innodb default CHARSET=utf8;

#create submission
create table submission(
	submisssion_id int(9) not null primary key auto_increment,
	mission_id int(9) not null,
	mission_order_id int(9) not null,
	`status` int(2) not null,
	content varchar(200) not null,
	remark varchar(200)
)engine=innodb default CHARSET=utf8;

alter table submission
add index s1(mission_id,mission_order_id);

#create person
create table person(
	person_id int(9) not null primary key auto_increment,
	`name` varchar(20) not null,
	`password` varchar(64) not null,
	department varchar(50) not null,
	title varchar(50) not null,
	role varchar(20) not null,
	`status` int(2) not null,
	remark varchar(200)
)engine=innodb default CHARSET=utf8;

#create daily_report
create table daily_report(
	report_id int(9) not null primary key auto_increment,
	report_date date not null,
	person_id int(9) not null
)engine=innodb default CHARSET=utf8;

#create report_description
create table report_describe(
	describe_id int(9) not null primary key auto_increment,
	report_id int(9) not null,
	report_order_id int(9) not null,
	mission_id int(9) not null,
	mission_order_id int(9) not null,
	content varchar(500)
)engine=innodb default CHARSET=utf8;

alter table report_describe
add index rd1(mission_id,mission_order_id);

#create submission-person 
create table submission_to_person(
	id int(9) not null primary key auto_increment,
	person_id int(9) not null,
	mission_id int(9) not null,
	mission_order_id int(9) not null
)engine=innodb default CHARSET=utf8;

alter table submission_to_person
add index sb_to_p1(person_id,mission_id,mission_order_id);

#create code for looking up status
create table `code`(
	`key` int(9) not null,
	`name` varchar(20) not null,
	`value` int(9) not null
)engine=innodb default CHARSET=utf8;
#fill code
insert into `code` 
values(0,'person',1),(0,'submission',2),
(1,'在职',1),(1,'休假',2),(1,'离职',3),
(2,'运行中',1),(2,'暂停',2),(2,'取消',3),(2,'完成',4);

