-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 20, 2026 at 12:12 PM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `house_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `advance_payments`
--

CREATE TABLE IF NOT EXISTS `advance_payments` (
  `advance_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `payment_type` varchar(50) NOT NULL,
  `reference_id` varchar(100) DEFAULT NULL,
  `account_number` varchar(50) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`advance_id`),
  KEY `advance_payments_ibfk_1` (`user_id`),
  KEY `advance_payments_ibfk_2` (`house_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `advance_payments`
--

INSERT INTO `advance_payments` (`advance_id`, `user_id`, `house_id`, `payment_type`, `reference_id`, `account_number`, `description`, `created_at`) VALUES
(4, 2, 7, 'gpay', 'dfdsfds543524543', '', '', '2026-01-20 17:30:12');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE IF NOT EXISTS `bookings` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `house_owner_id` int(11) NOT NULL,
  `booking_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_from` date NOT NULL,
  `date_to` date DEFAULT NULL,
  `status` enum('pending','accepted','declined') DEFAULT 'pending',
  `description` text,
  PRIMARY KEY (`booking_id`),
  KEY `house_id` (`house_id`),
  KEY `user_id` (`user_id`),
  KEY `house_owner_id` (`house_owner_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `house_id`, `user_id`, `house_owner_id`, `booking_date`, `date_from`, `date_to`, `status`, `description`) VALUES
(2, 7, 2, 1, '2026-01-20 17:25:15', '2026-02-01', '2026-12-20', 'accepted', 'ok ');

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE IF NOT EXISTS `contacts` (
  `contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `queries` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `info_response` varchar(255) DEFAULT NULL,
  `queries_response` text,
  PRIMARY KEY (`contact_id`),
  KEY `user_id` (`user_id`),
  KEY `house_id` (`house_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`contact_id`, `user_id`, `house_id`, `info`, `queries`, `created_at`, `info_response`, `queries_response`) VALUES
(2, 2, 7, 'hii', 'bill for water ?', '2026-01-20 17:25:29', 'ok', 'ok');

-- --------------------------------------------------------

--
-- Table structure for table `houses`
--

CREATE TABLE IF NOT EXISTS `houses` (
  `house_id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) DEFAULT NULL,
  `flat_number` varchar(50) DEFAULT NULL,
  `flat_name` varchar(100) DEFAULT NULL,
  `area_name` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `rent_per_month` int(11) DEFAULT NULL,
  `advance` int(11) DEFAULT NULL,
  `no_of_rooms` int(11) DEFAULT NULL,
  `no_of_bedrooms` int(11) DEFAULT NULL,
  `image1` varchar(255) NOT NULL,
  `image2` varchar(255) DEFAULT NULL,
  `image3` varchar(255) DEFAULT NULL,
  `image4` varchar(255) DEFAULT NULL,
  `image5` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`house_id`),
  KEY `owner_id` (`owner_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `houses`
--

INSERT INTO `houses` (`house_id`, `owner_id`, `flat_number`, `flat_name`, `area_name`, `location`, `pincode`, `rent_per_month`, `advance`, `no_of_rooms`, `no_of_bedrooms`, `image1`, `image2`, `image3`, `image4`, `image5`, `created_at`) VALUES
(5, 1, '77', NULL, 'rte', 'karadikadu', '638701', 5000, 30000, 5, 3, '2.png', '3.png', '1.png', '7.png', NULL, '2026-01-20 16:35:32'),
(7, 1, '77', 'qwerty', 'rte', 'covai', '638701', 5000, 25000, 5, 4, 'Screenshot_41.png', NULL, NULL, NULL, NULL, '2026-01-20 16:55:15');

-- --------------------------------------------------------

--
-- Table structure for table `owners`
--

CREATE TABLE IF NOT EXISTS `owners` (
  `house_owner_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`house_owner_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `owners`
--

INSERT INTO `owners` (`house_owner_id`, `name`, `email`, `mobile`, `password`, `location`) VALUES
(1, 'arun p1', 'arun@gmail.com', '9876543210', '123', 'valparai'),
(2, 'owner 1', 'ascentztech@gmail.com', '9543217860', '123', 'covai');

-- --------------------------------------------------------

--
-- Table structure for table `rent_payments`
--

CREATE TABLE IF NOT EXISTS `rent_payments` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `payment_type` varchar(50) NOT NULL,
  `reference_id` varchar(100) DEFAULT NULL,
  `account_number` varchar(50) DEFAULT NULL,
  `description` text,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`),
  KEY `user_id` (`user_id`),
  KEY `house_id` (`house_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `rent_payments`
--

INSERT INTO `rent_payments` (`payment_id`, `user_id`, `house_id`, `amount`, `payment_type`, `reference_id`, `account_number`, `description`, `image`, `created_at`) VALUES
(2, 2, 7, 5000, 'rupay', 'dfdsfds543524543', '', '', '1.png', '2026-01-20 17:30:30'),
(3, 2, 7, 5000, 'bank', '', 'qw234123456', '', NULL, '2026-01-20 17:32:17');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `mobile`, `password`, `location`) VALUES
(1, 'arun p1', 'arun@gmail.com', '9876543210', '123', 'valparai'),
(2, 'customer 1', 'kamalesh@gmail.com', '9876542310', '123', 'covai');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `advance_payments`
--
ALTER TABLE `advance_payments`
  ADD CONSTRAINT `advance_payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `advance_payments_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `houses` (`house_id`);

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `houses` (`house_id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`house_owner_id`) REFERENCES `owners` (`house_owner_id`);

--
-- Constraints for table `contacts`
--
ALTER TABLE `contacts`
  ADD CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `contacts_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `houses` (`house_id`);

--
-- Constraints for table `houses`
--
ALTER TABLE `houses`
  ADD CONSTRAINT `houses_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `owners` (`house_owner_id`);

--
-- Constraints for table `rent_payments`
--
ALTER TABLE `rent_payments`
  ADD CONSTRAINT `rent_payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `rent_payments_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `houses` (`house_id`);
