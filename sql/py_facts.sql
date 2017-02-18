-- phpMyAdmin SQL Dump
-- version 4.0.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 08, 2013 at 02:26 AM
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
-- Table structure for table `py_facts`
--

CREATE TABLE IF NOT EXISTS `py_facts` (
  `factname` varchar(255) NOT NULL,
  `factauthor` varchar(255) NOT NULL,
  `factlock` int(11) NOT NULL,
  `date` varchar(255) NOT NULL,
  `channel` varchar(255) NOT NULL,
  `fact` varchar(255) NOT NULL,
  UNIQUE KEY `factname` (`factname`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
