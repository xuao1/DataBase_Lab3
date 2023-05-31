/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023/5/29 21:12:45                           */
/*==============================================================*/

DROP DATABASE IF EXISTS lab3;
CREATE DATABASE lab3;
USE lab3;

/*==============================================================*/
/* Table: Course                                                */
/*==============================================================*/
create table Course
(
   CID                  char(32) not null  comment '',
   CName                char(128)  comment '',
   CHours               int  comment '',
   CType                int  comment '',
   primary key (CID)
);

/*==============================================================*/
/* Table: Paper                                                 */
/*==============================================================*/
create table Paper
(
   PaID                 int not null  comment '',
   PaName               char(128)  comment '',
   PaSource             char(128)  comment '',
   PaDate               int  comment '', 
   PaType               int  comment '',
   PaLevel              int  comment '',
   primary key (PaID)
);

/*==============================================================*/
/* Table: Project                                               */
/*==============================================================*/
create table Project
(
   ProID                char(32) not null  comment '',
   ProName              char(128)  comment '',
   ProSource            char(128)  comment '',
   ProType              int  comment '',
   ProBudget            float  comment '',
   ProStart             int  comment '',
   ProEnd               int  comment '',
   primary key (ProID)
);

/*==============================================================*/
/* Table: Teacher                                               */
/*==============================================================*/
create table Teacher
(
   TID                  char(5) not null  comment '',
   TName                char(32)  comment '',
   TSex                 int  comment '',
   TTitle               int  comment '',
   primary key (TID)
);

/*==============================================================*/
/* Table: Teacher_Course                                        */
/*==============================================================*/
create table Teacher_Course
(
   TID                  char(5) not null  comment '',
   CID                  char(32) not null  comment '',
   TCDate               int  comment '',
   TCTerm               int  comment '',
   TCHour               int  comment '',
   primary key (TID, CID, TCDate, TCTerm)
);

/*==============================================================*/
/* Table: Teacher_Paper                                         */
/*==============================================================*/
create table Teacher_Paper
(
   TID                  char(5) not null  comment '',
   PaID                 int not null  comment '',
   TPaRanking           int  comment '',
   TPaCA                bool  comment '',
   primary key (TID, PaID)
);

/*==============================================================*/
/* Table: Teacher_Project                                       */
/*==============================================================*/
create table Teacher_Project
(
   TID                  char(5) not null  comment '',
   ProID                char(32) not null  comment '',
   TProRanking          int  comment '',
   TProBudget           float  comment '',
   primary key (TID, ProID)
);

alter table Teacher_Course add constraint FK_Teacher_Course_TEACHER foreign key (TID)
      references Teacher (TID) on delete restrict on update restrict;

alter table Teacher_Course add constraint FK_Teacher_Course_COURSE foreign key (CID)
      references Course (CID) on delete restrict on update restrict;

alter table Teacher_Paper add constraint FK_Teacher_Paper_TEACHER foreign key (TID)
      references Teacher (TID) on delete restrict on update restrict;

alter table Teacher_Paper add constraint FK_Teacher_Paper_PAPER foreign key (PaID)
      references Paper (PaID) on delete restrict on update restrict;

alter table Teacher_Project add constraint FK_Teacher_Project_TEACHER foreign key (TID)
      references Teacher (TID) on delete restrict on update restrict;

alter table Teacher_Project add constraint FK_Teacher_Project_PROJECT foreign key (ProID)
      references Project (ProID) on delete restrict on update restrict;

