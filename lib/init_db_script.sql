-- create database luckybili default character set utf8mb4 collate utf8mb4_general_ci;
use luckybili;

create table t_draw_dynamic
(
    dyn_url     varchar(255) charset latin1 not null
        primary key,
    insert_time datetime                    null,
    source      varchar(255) charset latin1 null,
    note        varchar(255)                null,
    status      varchar(20)                 null
)
    collate = utf8_bin;

create table t_followdups
(
    id          int auto_increment
        primary key,
    up_id       varchar(255) null,
    up_url      varchar(255) null,
    status      int          null,
    update_time datetime     null,
    user_id     varchar(50)  null
)
    comment '关注的up主信息';

create table t_prize
(
    id        int auto_increment
        primary key,
    status    int          null,
    prize_url varchar(255) null,
    user_id   varchar(50)  null
)
    comment '中奖信息表';

create table t_share_info
(
    id           int auto_increment,
    share_url    varchar(255) null,
    status       int          not null comment '当前动态状态',
    upId         varchar(50)  null,
    upUrl        varchar(255) null,
    machine_ip   varchar(20)  null,
    share_time   datetime     null,
    share_status int          null,
    user_id      varchar(50)  null,
    constraint t_share_info_pk
        unique (id)
)
    comment '动态转发的基本信息表';

create table t_shared_urls
(
    dyn_url     varchar(255) not null,
    insert_time datetime     null,
    update_time datetime     null,
    status      varchar(50)  null,
    user_id     varchar(20)  not null,
    primary key (user_id, dyn_url)
);

create table t_statistics
(
    id          int auto_increment
        primary key,
    content     varchar(255) collate utf8_bin null,
    insert_time datetime                      null,
    note        varchar(500) collate utf8_bin null comment '备注',
    user_id     varchar(50)                   null
);

