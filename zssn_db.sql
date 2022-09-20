CREATE TABLE `survivor` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(64) NOT NULL,
	`age` int(3) NOT NULL,
	`gender` char(1) NOT NULL,
	`location` point(255) NOT NULL,
	`infected` int NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE `inventory` (
	`id` int NOT NULL AUTO_INCREMENT,
	`item_id` int NOT NULL,
	`amount` int NOT NULL,
	`survivor_id` int NOT NULL,
	`bag_index` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `items` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(64) NOT NULL AUTO_INCREMENT,
	`value` char(1) NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `inventory` ADD CONSTRAINT `inventory_fk0` FOREIGN KEY (`item_id`) REFERENCES `items`(`id`);

ALTER TABLE `inventory` ADD CONSTRAINT `inventory_fk1` FOREIGN KEY (`survivor_id`) REFERENCES `survivor`(`id`);




