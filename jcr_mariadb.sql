CREATE TABLE IF NOT EXISTS `journal` (
	`jid` INT(8) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`issn` CHAR(9) NOT NULL,
	`title` VARCHAR(255) NOT NULL,
	`abbrev` VARCHAR(100) NOT NULL,
	`isoAbbrev` VARCHAR(100) NOT NULL,
	`jcrAbbrev` VARCHAR(100) NOT NULL,
	`factor` FLOAT(7,3),
	`fiveFactor` FLOAT(7,3),
	`issue` SMALLINT(4) UNSIGNED,
	`articleNum` INT(7) UNSIGNED,
	`citeNum` INT(8) UNSIGNED,
	`halfLife` VARCHAR(10),
	`immediacyIndex` FLOAT(7,3),
	`eigenFactor` FLOAT(9, 5),
	`influenceScore` FLOAT(7, 3),
	`homepage` VARCHAR(255),
	`authorLink` VARCHAR(255),
	`viewNum` INT(10) UNSIGNED DEFAULT 0
) ENGINE=InnoDB AUTO_INCREMENT = 518404;

CREATE TABLE IF NOT EXISTS `addition` (
	`aid` INT(8) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(200) NOT NULL,
	`type` VARCHAR(20),
	`note` VARCHAR(255),
	`journalNum` INT(7) UNSIGNED
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `category` (
	`aid` INT(8) UNSIGNED NOT NULL,
	`medianFactor` FLOAT(7,3),
	`aggregateFactor` FLOAT(7,3),
	`immediacyIndex` FLOAT(7,3),
	`halfLife` VARCHAR(10),
	`citeNum` INT(8) UNSIGNED,
	`articleNum` INT(7) UNSIGNED
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `relationship` (
	`jid` INT(8) UNSIGNED,
	`rid` INT(8) UNSIGNED
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `history` (
	`jid` INT(8) UNSIGNED NOT NULL,
	`year` SMALLINT(4) UNSIGNED NOT NULL,
	`factor` FLOAT(7,3),
	`fiveFactor` FLOAT(7,3),
	`immediacyIndex` FLOAT(7,3),
	`eigenFactor` FLOAT(9, 5),
	`influenceScore` FLOAT(7, 3),
	`halfLife` VARCHAR(10),
	`articleNum` INT(7) UNSIGNED,
	`citeNum` INT(8) UNSIGNED
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `user` (
	`uid` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`email` VARCHAR(200) NOT NULL,
	`name` VARCHAR(32),
	`password` CHAR(40) NOT NULL,
	`type` TINYINT(2) UNSIGNED,
	`created` INT(10) UNSIGNED NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT = 180765;

CREATE TABLE IF NOT EXISTS `comment` (
	`cid` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`jid` INT(8) UNSIGNED NOT NULL,
	`uid` INT(10) UNSIGNED NOT NULL,
	`content` TEXT,
	`parent` INT(10) UNSIGNED DEFAULT 0,
	`ip` VARCHAR(15),
	`approved` TINYINT(1) DEFAULT 0,
	`agent` VARCHAR(255),
	`review` TINYINT(2),
	`submit` TINYINT(1),
	`created` INT(10) UNSIGNED NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `focus` (
	`uid` INT(10) UNSIGNED NOT NULL,
	`jid` SMALLINT(5) UNSIGNED NOT NULL,
	`created` INT(10) UNSIGNED NOT NULL
) ENGINE=InnoDB;