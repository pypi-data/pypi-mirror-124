-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2020 年 02 月 02 日 05:49
-- 伺服器版本： 8.0.17
-- PHP 版本： 7.2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `moon`
--
CREATE DATABASE IF NOT EXISTS `moon` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `moon`;

-- --------------------------------------------------------

--
-- 資料表結構 `Invoice`
--

CREATE TABLE `Invoice` (
  `Invoice_id` int(11) NOT NULL,
  `Invoice_name` varchar(11) NOT NULL,
  `Shop_name` varchar(20) NOT NULL,
  `Payment_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 資料表結構 `Item`
--

CREATE TABLE `Item` (
  `Item_id` int(11) NOT NULL,
  `Invoice_ID` int(11) NOT NULL,
  `Item_num` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Points` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 資料表結構 `Payment`
--

CREATE TABLE `Payment` (
  `Payment_id` int(11) NOT NULL,
  `Invoice_ID` varchar(20) NOT NULL,
  `Payment_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Payment_price` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `Invoice`
--
ALTER TABLE `Invoice`
  ADD PRIMARY KEY (`Invoice_id`),
  ADD UNIQUE KEY `Invoice_name` (`Invoice_name`),
  ADD UNIQUE KEY `Payment_ID` (`Payment_ID`) USING BTREE,
  ADD KEY `Shop_name` (`Shop_name`);

--
-- 資料表索引 `Item`
--
ALTER TABLE `Item`
  ADD PRIMARY KEY (`Item_id`),
  ADD KEY `Points` (`Points`),
  ADD KEY `Invoice_ID` (`Invoice_ID`),
  ADD KEY `Item_num` (`Item_num`) USING BTREE;

--
-- 資料表索引 `Payment`
--
ALTER TABLE `Payment`
  ADD PRIMARY KEY (`Payment_id`) USING BTREE,
  ADD KEY `Invoice_ID` (`Invoice_ID`),
  ADD KEY `Payment_name` (`Payment_name`) USING BTREE,
  ADD KEY `Payment_price` (`Payment_price`) USING BTREE;

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `Invoice`
--
ALTER TABLE `Invoice`
  MODIFY `Invoice_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `Item`
--
ALTER TABLE `Item`
  MODIFY `Item_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `Invoice`
--
ALTER TABLE `Invoice`
  ADD CONSTRAINT `Invoice_ibfk_1` FOREIGN KEY (`Payment_ID`) REFERENCES `Payment` (`Payment_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- 資料表的限制式 `Item`
--
ALTER TABLE `Item`
  ADD CONSTRAINT `Item_ibfk_1` FOREIGN KEY (`Invoice_ID`) REFERENCES `Invoice` (`Invoice_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
