-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2020 年 02 月 02 日 09:24
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

--
-- 傾印資料表的資料 `Invoice`
--

INSERT INTO `Invoice` (`Invoice_id`, `Invoice_name`, `Shop_name`, `Payment_ID`) VALUES
(1, 'WH-89255079', 'Donutes(德賢) ', 1),
(2, 'WP-28969362', '極品豚骨拉麵店', 2),
(3, 'VZ-00301065', '7-11(德賢)', 3),
(4, 'WH-89258679', 'Donutes(德賢)', 4),
(5, 'VZ-00301466', '7-11(德賢)', 5),
(6, 'VM-05045438', '小北百貨(楠梓)', 6),
(7, 'WH-89319039', 'Donutes(德賢)', 7),
(8, 'VM-05089116', '小北百貨(楠梓)', 8),
(9, 'VM-05089133', '小北百貨(楠梓)', 9),
(10, 'WM-4089993', 'McDonald\'s(後勁)', 10),
(11, 'WH-89260141', 'Donutes(德賢)', 11),
(12, 'WM-54095660', 'McDonald\'s(後勁)', 12),
(13, 'VZ-00310441', '7-11(德賢)', 13);

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

--
-- 傾印資料表的資料 `Item`
--

INSERT INTO `Item` (`Item_id`, `Invoice_ID`, `Item_num`, `Points`) VALUES
(1, 1, '葡萄奶酥炸彈', 28),
(2, 1, '聖誕夜之星', 35),
(3, 1, '聖誕夜之星', 35),
(4, 2, '混沌拉麵', 85),
(5, 3, '純喫茶紅茶650ml', 25),
(6, 4, '波羅', 25),
(7, 4, '葡萄奶酥炸彈', 28),
(8, 4, '黑糖杯杯', 28),
(9, 5, '瑞穗麥芽牛奶', 42),
(10, 6, '黑人牙膏', 64),
(11, 7, '波羅 ', 50),
(12, 7, '波羅 ', 50),
(13, 8, 'H20純水家庭號', 45),
(14, 9, '防寒手套', 99),
(15, 10, '經典中薯', 17),
(16, 10, '加購六塊雞', 55),
(17, 10, '嫩煎雞腿堡', 82),
(18, 10, '雪碧', 33),
(19, 11, '波羅麵包', 25),
(20, 11, '波羅麵包', 25),
(21, 11, '波羅麵包', 25),
(22, 11, '波羅麵包', 25),
(23, 12, '50點換大薯', 0),
(24, 3, '舒潔棉柔小熊維尼版', 100),
(25, 3, '舒潔棉柔小熊維泥版', 100);

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
-- 傾印資料表的資料 `Payment`
--

INSERT INTO `Payment` (`Payment_id`, `Invoice_ID`, `Payment_name`, `Payment_price`) VALUES
(1, '2019-11-25 23:12:03', '現金', 1),
(2, '2019-12-02 18:31:12', '現金', 0),
(3, '2019-12-03 18:28:20', '悠遊卡', 0),
(4, '2019-12-03 22:44:42', '現金', 0),
(5, '2019-12-04 18:13:23', '悠遊卡', 0),
(6, '2019-12-04 8:08:00', '悠遊卡', 0),
(7, '2019-12-07 12:28:57', '現金', 1),
(8, '2019-12-07 12:34:00', '悠遊卡', 0),
(9, '2019-12-04 23:59:00', '現金', 0),
(10, '2019-12-09 22:37:19', 'Mcard(點點卡)', 18),
(11, '2019-12-10 20:06:46', '現金', 2),
(12, '2019-12-16 22:50:21', 'Mcard(點點卡)', -50),
(13, '2019-12-18 23:30:44', '悠遊卡', 3);

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
  MODIFY `Item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

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
