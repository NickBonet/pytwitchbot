-- phpMyAdmin SQL Dump
-- version 4.0.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 07, 2013 at 12:56 AM
-- Server version: 5.5.30-log
-- PHP Version: 5.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `pyircbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `py_users`
--

CREATE TABLE IF NOT EXISTS `py_users` (
  `nick` varchar(255) NOT NULL,
  `ident` varchar(255) NOT NULL,
  `host` varchar(255) NOT NULL,
  `passphrase` varchar(255) NOT NULL,
  `level` int(11) NOT NULL,
  UNIQUE KEY `nick` (`nick`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
