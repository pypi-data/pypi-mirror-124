-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2020 年 03 月 08 日 09:02
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

--
-- 傾印資料表的資料 `invoice`
--

INSERT INTO `invoice` (`id`, `Invoice`, `location`, `Payment_ID`) VALUES
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

--
-- 傾印資料表的資料 `item`
--

INSERT INTO `item` (`id`, `Invoice_ID`, `item`, `money`) VALUES
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

--
-- 傾印資料表的資料 `payment`
--

INSERT INTO `payment` (`id`, `date`, `payment`, `points`) VALUES
(3, '2019-12-03 18:28:20', '悠遊卡', 0),
(4, '2019-12-03 22:44:42', '現金', 0),
(5, '2019-12-04 18:13:23', '悠遊卡', 0),
(6, '2019-12-04 08:08:00', '悠遊卡', 0),
(7, '2019-12-07 12:28:57', '現金', 1),
(8, '2019-12-07 12:34:00', '悠遊卡', 0),
(9, '2019-12-04 23:59:00', '現金', 0),
(10, '2019-12-09 22:37:19', 'Mcard(點點卡)', 18),
(11, '2019-12-10 20:06:46', '現金', 2),
(12, '2019-12-16 22:50:21', 'Mcard(點點卡)', -50),
(13, '2019-12-18 23:30:44', '悠遊卡', 3);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
