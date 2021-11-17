CREATE TABLE `environment` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `environment_name` varchar(512),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `page` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `page_id` int(11) UNIQUE,
    `environment_id` int(11),
    `page_title` varchar(512),
    `last_check_time` datetime,
    PRIMARY KEY (`id`),
    CONSTRAINT `environment_id_fk` FOREIGN KEY (`environment_id`) REFERENCES `environment` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `user_id` int(11) UNIQUE,
    `user_name` varchar(512),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `revision` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `rev_id` int(11) UNIQUE,
    `page_id` int(11),
    `user_id` int(11),
    `rev_date` datetime,
    `prev_rev` int(11),
    `text_retrieved` boolean,
    `last_attempt_date` datetime,
    `num_attempts` integer,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `revision_log` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `version` int(11),
    `stage` int(11),
    `page_id` int(11),
    `last_rev` int(11),
    `lock_date` datetime,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `user_reputation` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `version` int(11),
    `user_id` int(11),
    `environment` int(11),
    `reputation_value` double,
    PRIMARY KEY (`id`),
    CONSTRAINT `environment_id_usr_rep` FOREIGN KEY (`environment`) REFERENCES `environment` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `text_storage` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `version` int(11),
    `page_id` int(11),
    `rev_id` int(11),
    `text_type` varchar(512),
    `blob` varchar(512),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `triangles` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `version` int(11),
    `page_id` int(11),
    `rev_id_1` int(11),
    `rev_id_2` int(11),
    `rev_id_3` int(11),
    `reputation_inc` double,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `text_diff` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `version` int(11),
    `rev_id_1` int(11),
    `rev_id_2` int(11),
    `info` text,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `text_distance` (
    `id` int(11) AUTO_INCREMENT NOT NULL,
    `version` int(11),
    `rev_id_1` int(11),
    `rev_id_2` int(11),
    `distance` double,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;