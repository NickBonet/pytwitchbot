-- phpMyAdmin SQL Dump
-- version 4.0.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 06, 2013 at 10:59 PM
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
-- Table structure for table `py_quotes`
--

CREATE TABLE IF NOT EXISTS `py_quotes` (
  `qid` int(11) NOT NULL AUTO_INCREMENT,
  `qchid` int(11) NOT NULL,
  `qnick` varchar(255) NOT NULL,
  `qchan` varchar(255) NOT NULL,
  `qdate` varchar(255) NOT NULL,
  `quote` varchar(255) NOT NULL,
  PRIMARY KEY (`qid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
