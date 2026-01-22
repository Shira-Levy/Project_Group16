-- Database Export for flytau_db

CREATE DATABASE IF NOT EXISTS flytau_db;
USE flytau_db;

SET FOREIGN_KEY_CHECKS=0;

-- Table structure for table `airplane`
DROP TABLE IF EXISTS `airplane`;
CREATE TABLE `airplane` (
  `A_ID` int NOT NULL,
  `Manufacturer` varchar(45) DEFAULT NULL,
  `Date_of_Purchase` date DEFAULT NULL,
  `Size` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`A_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `airplane`
INSERT INTO `airplane` VALUES 
(1, 'Airbus', '2018-03-15', 'Large'),
(2, 'Boeing', '2019-07-01', 'Small'),
(3, 'Dassault', '2020-01-20', 'Small'),
(4, 'Airbus', '2017-11-05', 'Large'),
(5, 'Boeing', '2016-05-30', 'Small'),
(6, 'Dassault', '2021-09-10', 'Small');

-- Table structure for table `airport`
DROP TABLE IF EXISTS `airport`;
CREATE TABLE `airport` (
  `Airport_Name` varchar(45) NOT NULL,
  `Country` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Airport_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `airport`
INSERT INTO `airport` VALUES 
('Ataturk', 'Turkey'),
('Ben Gurion', 'Israel'),
('Charles de Gaulle', 'France'),
('Dubai Int', 'UAE'),
('Heathrow', 'United Kingdom'),
('JFK', 'USA'),
('Los Angeles Int', 'USA'),
('Schiphol', 'Netherlands'),
('Sydney Kingsford', 'Australia'),
('Tokyo Haneda', 'Japan'),
('Toronto Pearson', 'Canada');

-- Table structure for table `booking`
DROP TABLE IF EXISTS `booking`;
CREATE TABLE `booking` (
  `B_ID` int NOT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Price` int DEFAULT NULL,
  `Cancellation_Fee` int DEFAULT NULL,
  `booking_date` date DEFAULT NULL,
  `booking_time` time DEFAULT NULL,
  `Client_Email` varchar(45) NOT NULL,
  PRIMARY KEY (`B_ID`),
  KEY `fk_client` (`Client_Email`) /*!80000 INVISIBLE */,
  CONSTRAINT `fk_Client` FOREIGN KEY (`Client_Email`) REFERENCES `client` (`Email_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `booking`
INSERT INTO `booking` VALUES 
(1, 'Cancelled', 100, 100, '2025-05-01', '08:00:00', 'reg1@flytau.com'),
(2, 'Confirmed', 2000, 100, '2025-05-01', '08:10:00', 'reg2@flytau.com'),
(3, 'Cancelled', 50, 50, '2025-05-02', '09:00:00', 'guest1@example.com'),
(4, 'Confirmed', 1000, 50, '2025-05-02', '09:05:00', 'guest2@example.com'),
(5, 'Cancelled', 50, 50, '2025-05-03', '10:00:00', 'reg1@flytau.com'),
(6, 'Confirmed', 1000, 50, '2025-05-03', '10:05:00', 'reg2@flytau.com'),
(7, 'Cancelled', 50, 50, '2025-05-04', '11:00:00', 'guest1@example.com'),
(8, 'Confirmed', 1000, 50, '2025-05-04', '11:02:00', 'guest2@example.com'),
(15, 'Confirmed', 2000, 100, '2025-12-27', '18:54:59', 'reg1@flytau.com'),
(16, 'Confirmed', 1000, 50, '2025-12-27', '18:58:07', 'reg1@flytau.com'),
(17, 'Confirmed', 1000, 50, '2025-12-27', '19:01:05', 'reg1@flytau.com'),
(18, 'Confirmed', 1000, 50, '2025-12-27', '19:02:05', 'reg1@flytau.com'),
(21, 'Confirmed', 2000, 100, '2026-01-06', '15:32:11', 'reg1@flytau.com'),
(22, 'Confirmed', 1000, 50, '2026-01-06', '18:15:59', 'shiralevy2017@gmail.com'),
(23, 'Confirmed', 1000, 50, '2026-01-13', '16:19:06', 'shiralevy2017@gmail.com'),
(24, 'Manager Cancelled', 0, 0, '2026-01-13', '17:44:24', 'shiralevy2017@gmail.com'),
(25, 'Manager Cancelled', 0, 0, '2026-01-14', '14:16:41', 'shiralevy2017@gmail.com'),
(26, 'Manager Cancelled', 0, 0, '2026-01-14', '16:52:42', 'inbal@mon'),
(27, 'Manager Cancelled', 0, 0, '2026-01-14', '17:13:41', 'shiralevy2017@gmail.com'),
(28, 'Confirmed', 4500, 225, '2026-01-14', '18:03:21', 'guest@mail'),
(29, 'Manager Cancelled', 0, 0, '2026-01-15', '16:54:25', 'shiralevy2017@gmail.com'),
(30, 'Cancelled', 163, 163, '2026-01-19', '20:27:36', 'shiralevy2017@gmail.com'),
(31, 'Cancelled', 145, 145, '2026-01-20', '10:53:18', 'osher@melich'),
(32, 'Confirmed', 1000, 50, '2026-01-20', '11:44:23', 'shiralevy2017@gmail.com'),
(33, 'Confirmed', 1000, 50, '2026-01-20', '11:50:15', 'osher@melich'),
(34, 'Confirmed', 5000, 250, '2026-01-20', '12:28:47', 'shiralevy2017@gmail.com'),
(35, 'Confirmed', 1000, 50, '2026-01-20', '15:18:19', 'shmulik@cohen'),
(36, 'Confirmed', 1000, 50, '2026-01-20', '15:20:21', 'shmulik@cohen'),
(37, 'Confirmed', 1000, 50, '2026-01-20', '15:38:45', 'shmulik@cohen'),
(38, 'Confirmed', 5000, 250, '2026-01-20', '18:16:54', 'inbal@mon'),
(39, 'Confirmed', 3600, 180, '2026-01-20', '20:02:00', 'inbal@mon'),
(40, 'Cancelled', 180, 180, '2026-01-20', '20:40:33', 'yonatan@hakatan'),
(41, 'Confirmed', 1700, 85, '2026-01-20', '20:44:50', 'monkey@luffy');

-- Table structure for table `class`
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `Type` varchar(45) NOT NULL,
  `Num_Rows` int NOT NULL,
  `Num_Columns` int NOT NULL,
  `A_ID` int NOT NULL,
  PRIMARY KEY (`A_ID`,`Type`),
  KEY `fk_Class_Airplane1_idx` (`A_ID`),
  CONSTRAINT `fk_Class` FOREIGN KEY (`A_ID`) REFERENCES `airplane` (`A_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `class`
INSERT INTO `class` VALUES 
('Business', 5, 4, 1),
('Economy', 20, 6, 1),
('Economy', 18, 6, 2),
('Economy', 15, 4, 3),
('Business', 5, 4, 4),
('Economy', 20, 6, 4),
('Economy', 18, 6, 5),
('Economy', 12, 4, 6);

-- Table structure for table `client`
DROP TABLE IF EXISTS `client`;
CREATE TABLE `client` (
  `Email_ID` varchar(45) NOT NULL,
  PRIMARY KEY (`Email_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `client`
INSERT INTO `client` VALUES 
('elad@bensh'),
('guest1@example.com'),
('guest2@example.com'),
('guest@mail'),
('inbal@mon'),
('manager1@flytau.com'),
('manager2@flytau.com'),
('monkey@luffy'),
('osher@melich'),
('reg1@flytau.com'),
('reg2@flytau.com'),
('shir@lev'),
('shiralevy2017@gmail.com'),
('shmulik@cohen'),
('yonatan@hakatan');

-- Table structure for table `employee`
DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
  `E_ID` int NOT NULL,
  `PhoneNumber` varchar(20) DEFAULT NULL,
  `StartDateofEmployment` date DEFAULT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `City` varchar(45) DEFAULT NULL,
  `Street` varchar(45) CHARACTER SET armscii8 COLLATE armscii8_general_ci DEFAULT NULL,
  `HoushNumber` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`E_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `employee`
INSERT INTO `employee` VALUES 
(1, '972501111111', '2015-01-01', 'דנה', 'לוי', 'Tel Aviv', 'Herzl', '10'),
(2, '972502222222', '2016-02-15', 'יוסי', 'כהן', 'Jerusalem', 'Jabotinsky', '5'),
(3, '972503000001', '2017-03-10', 'עמית', 'רונן', 'Haifa', 'HaAliya', '12'),
(4, '972503000002', '2017-04-20', 'נועם', 'בר', 'Haifa', 'Hanassi', '7'),
(5, '972503000003', '2018-05-11', 'רוני', 'כץ', 'Ashdod', 'Begin', '3'),
(6, '972503000004', '2018-06-01', 'אלי', 'פרץ', 'Beer Sheva', 'Rager', '22'),
(7, '972503000005', '2019-01-01', 'ליאור', 'שלו', 'Eilat', 'Derech HaYam', '1'),
(8, '972503000006', '2019-02-02', 'תמר', 'גרוס', 'Tel Aviv', 'Ibn Gabirol', '23'),
(9, '972503000007', '2020-03-03', 'גיל', 'אמסלם', 'Holon', 'Sokolov', '9'),
(10, '972503000008', '2020-04-04', 'יעל', 'אביב', 'Ramat Gan', 'Krinitzi', '18'),
(11, '972503000009', '2021-05-05', 'ניר', 'שלמה', 'Netanya', 'Weizmann', '4'),
(12, '972503000010', '2021-06-06', 'עומר', 'זיו', 'Ashkelon', 'Hahagana', '16'),
(13, '972504000001', '2019-01-01', 'שיר', 'מור', 'Tel Aviv', 'Frishman', '8'),
(14, '972504000002', '2019-01-15', 'לי', 'חן', 'Haifa', 'Levontin', '2'),
(15, '972504000003', '2019-02-01', 'עדי', 'טל', 'Ashdod', 'Jabotinsky', '11'),
(16, '972504000004', '2019-02-10', 'אודיה', 'רז', 'Eilat', 'Tarshish', '6'),
(17, '972504000005', '2020-03-01', 'בר', 'שני', 'Jerusalem', 'King George', '19'),
(18, '972504000006', '2020-03-10', 'הילה', 'בן ארי', 'Holon', 'Sokolov', '25'),
(19, '972504000007', '2020-04-01', 'טל', 'מזרחי', 'Beer Sheva', 'Smilanski', '7'),
(20, '972504000008', '2020-04-10', 'מור', 'לוי', 'Ashkelon', 'Hahistadrut', '30'),
(21, '972504000009', '2020-05-01', 'ירדן', 'רוזן', 'Haifa', 'Hagibor', '13'),
(22, '972504000010', '2020-05-10', 'אור', 'שחר', 'Tel Aviv', 'Rothschild', '21'),
(23, '972504000011', '2021-06-01', 'נוגה', 'Hadad', 'Rishon', 'Herzl', '6'),
(24, '972504000012', '2021-06-10', 'תום', 'ארבל', 'Ramat Gan', 'Bialik', '29'),
(25, '972504000013', '2021-07-01', 'אלעד', 'כרמל', 'Netanya', 'Dizengoff', '5'),
(26, '972504000014', '2021-07-10', 'רעות', 'שגיא', 'Ashdod', 'Herzl', '17'),
(27, '972504000015', '2022-08-01', 'גיא', 'אורן', 'Haifa', 'Allenby', '4'),
(28, '972504000016', '2022-08-10', 'נעמה', 'קורן', 'Tel Aviv', 'King George', '14'),
(29, '972504000017', '2022-09-01', 'אופיר', 'שני', 'Holon', 'Haatzmaut', '9'),
(30, '972504000018', '2022-09-10', 'מאי', 'Barak', 'Bat Yam', 'Balfour', '12'),
(31, '972504000019', '2023-01-01', 'איתי', 'שלום', 'Jerusalem', 'Jaffa', '20'),
(32, '972504000020', '2023-01-10', 'רומי', 'דיין', 'Beer Sheva', 'Herzl', '2'),
(33, '0505555555', '2026-01-13', 'ענבל', 'מונדייב', 'tel aviv', 'dizi', '57'),
(35, '05011111111', '2026-01-20', 'יוסי', 'כהן', 'jerusalem', 'gold', '11');

-- Table structure for table `flight`
DROP TABLE IF EXISTS `flight`;
CREATE TABLE `flight` (
  `F_ID` int NOT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  `Date_of_flight` date DEFAULT NULL,
  `Time_of_flight` time NOT NULL,
  `Date_of_Arrival` date DEFAULT NULL,
  `Time_of_Arrival` time NOT NULL,
  `A_ID` int NOT NULL,
  `R_ID` int NOT NULL,
  PRIMARY KEY (`F_ID`),
  KEY `FK_Flight_Airplane_idx` (`A_ID`),
  KEY `FK_Flight_Route _idx` (`R_ID`),
  CONSTRAINT `FK_Flight_Airplane` FOREIGN KEY (`A_ID`) REFERENCES `airplane` (`A_ID`),
  CONSTRAINT `FK_Flight_Route ` FOREIGN KEY (`R_ID`) REFERENCES `route` (`R_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `flight`
INSERT INTO `flight` VALUES 
(1, 'Completed', 'Short', '2025-06-01', '08:00:00', '2025-06-01', '13:00:00', 1, 1),
(2, 'Completed', 'Long', '2025-06-01', '23:00:00', '2025-06-02', '06:00:00', 4, 2),
(3, 'Completed', 'Short', '2025-06-02', '10:00:00', '2025-06-02', '14:00:00', 1, 3),
(4, 'Completed', 'Short', '2025-06-03', '09:00:00', '2025-06-03', '13:00:00', 2, 4),
(5, 'Completed', 'Short', '2025-06-04', '07:00:00', '2025-06-04', '11:00:00', 3, 5),
(6, 'Completed', 'Short', '2025-06-05', '12:00:00', '2025-06-05', '16:00:00', 1, 1),
(7, 'Cancelled', 'Short', '2026-02-10', '10:00:00', '2026-02-10', '15:00:00', 1, 1),
(8, 'Active', 'Long', '2026-02-10', '10:00:00', '2026-02-10', '21:00:00', 1, 2),
(9, 'Active', 'Short', '2026-02-10', '10:00:00', '2026-02-10', '14:00:00', 1, 3),
(10, 'Active', 'Long', '2026-02-10', '10:00:00', '2026-02-10', '17:00:00', 1, 4),
(11, 'Active', 'Long', '2026-02-10', '10:00:00', '2026-02-10', '18:00:00', 1, 5),
(12, 'Cancelled', 'Short', '2026-07-14', '10:00:00', '2026-07-14', '15:00:00', 3, 1),
(13, 'Active', 'Short', '2026-01-14', '10:30:00', '2026-01-14', '15:30:00', 2, 1),
(14, 'Cancelled', 'Short', '2026-02-14', '10:20:00', '2026-02-14', '15:20:00', 1, 1),
(15, 'Active', 'Short', '2026-02-14', '11:00:00', '2026-02-14', '15:00:00', 1, 3),
(16, 'Cancelled', 'Long', '2026-02-14', '10:00:00', '2026-02-14', '21:00:00', 1, 2),
(17, 'Active', 'Short', '2026-02-15', '10:00:00', '2026-02-15', '15:00:00', 1, 1),
(18, 'Active', 'Short', '2026-01-14', '11:00:00', '2026-01-14', '16:00:00', 1, 1),
(19, 'Active', 'Long', '2026-01-30', '10:00:00', '2026-01-30', '18:00:00', 1, 5),
(20, 'Active', 'Short', '2026-01-15', '14:30:00', '2026-01-15', '17:30:00', 2, 10),
(21, 'Active', 'Long', '2026-01-30', '10:22:00', '2026-01-30', '19:22:00', 1, 12),
(22, 'Active', 'Short', '2026-01-21', '10:56:00', '2026-01-21', '13:56:00', 1, 10),
(23, 'Active', 'Long', '2026-01-21', '11:32:00', '2026-01-21', '20:32:00', 1, 12),
(24, 'Active', 'Short', '2026-01-21', '11:42:00', '2026-01-21', '16:42:00', 2, 1),
(25, 'Active', 'Long', '2026-01-23', '12:27:00', '2026-01-23', '19:27:00', 1, 6),
(26, 'Active', 'Long', '2026-01-30', '18:09:00', '2026-01-31', '01:09:00', 4, 15),
(27, 'Cancelled', 'Short', '2026-01-28', '17:08:00', '2026-01-28', '20:08:00', 3, 10),
(28, 'Active', 'Short', '2026-01-30', '20:14:00', '2026-01-31', '01:14:00', 3, 9),
(29, 'Active', 'Short', '2026-01-30', '19:18:00', '2026-01-30', '23:18:00', 6, 3),
(30, 'Active', 'Short', '2026-01-22', '21:25:00', '2026-01-23', '02:25:00', 6, 9),
(31, 'Active', 'Long', '2026-03-23', '22:31:00', '2026-03-24', '05:31:00', 4, 15);

-- Table structure for table `flight_attendant`
DROP TABLE IF EXISTS `flight_attendant`;
CREATE TABLE `flight_attendant` (
  `E_ID` int NOT NULL,
  `Training_for_long_flights` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`E_ID`),
  CONSTRAINT `FK_FlightAttendant_Employee` FOREIGN KEY (`E_ID`) REFERENCES `employee` (`E_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `flight_attendant`
INSERT INTO `flight_attendant` VALUES 
(13, 'Yes'),
(14, 'Yes'),
(15, 'Yes'),
(16, 'No'),
(17, 'Yes'),
(18, 'No'),
(19, 'Yes'),
(20, 'No'),
(21, 'Yes'),
(22, 'Yes'),
(23, 'No'),
(24, 'Yes'),
(25, 'Yes'),
(26, 'No'),
(27, 'Yes'),
(28, 'Yes'),
(29, 'No'),
(30, 'Yes'),
(31, 'No'),
(32, 'Yes'),
(35, 'Yes');

-- Table structure for table `flight_class_price`
DROP TABLE IF EXISTS `flight_class_price`;
CREATE TABLE `flight_class_price` (
  `F_ID` int NOT NULL,
  `Seat_Class_Type` varchar(20) NOT NULL,
  `Ticket_Price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`F_ID`,`Seat_Class_Type`),
  CONSTRAINT `fk_fcp_flight` FOREIGN KEY (`F_ID`) REFERENCES `flight` (`F_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `flight_class_price`
INSERT INTO `flight_class_price` VALUES 
(1, 'Business', '2000.00'),
(1, 'Economy', '1000.00'),
(2, 'Business', '2000.00'),
(2, 'Economy', '1000.00'),
(3, 'Business', '2000.00'),
(3, 'Economy', '1000.00'),
(4, 'Economy', '1000.00'),
(5, 'Economy', '1000.00'),
(6, 'Business', '2000.00'),
(6, 'Economy', '1000.00'),
(7, 'Business', '2000.00'),
(7, 'Economy', '1000.00'),
(8, 'Business', '2000.00'),
(8, 'Economy', '1000.00'),
(9, 'Business', '2000.00'),
(9, 'Economy', '1000.00'),
(10, 'Business', '2000.00'),
(10, 'Economy', '1000.00'),
(11, 'Business', '2000.00'),
(11, 'Economy', '1000.00'),
(12, 'Economy', '1000.00'),
(13, 'Economy', '1000.00'),
(14, 'Business', '2000.00'),
(14, 'Economy', '1000.00'),
(15, 'Business', '2000.00'),
(15, 'Economy', '1000.00'),
(16, 'Business', '2000.00'),
(16, 'Economy', '1000.00'),
(17, 'Business', '1200.00'),
(17, 'Economy', '850.00'),
(18, 'Business', '1300.00'),
(18, 'Economy', '900.00'),
(19, 'Business', '1000.00'),
(19, 'Economy', '800.00'),
(20, 'Economy', '1500.00'),
(21, 'Business', '1150.00'),
(21, 'Economy', '850.00'),
(22, 'Business', '2500.00'),
(22, 'Economy', '1800.00'),
(23, 'Business', '2000.00'),
(23, 'Economy', '1000.00'),
(24, 'Economy', '1000.00'),
(25, 'Business', '1200.00'),
(25, 'Economy', '2500.00'),
(26, 'Business', '2500.00'),
(26, 'Economy', '1300.00'),
(27, 'Economy', '1200.00'),
(28, 'Economy', '1200.00'),
(29, 'Economy', '1200.00'),
(30, 'Economy', '1000.00'),
(31, 'Business', '3000.00'),
(31, 'Economy', '1200.00');

-- Table structure for table `flight_crew`
DROP TABLE IF EXISTS `flight_crew`;
CREATE TABLE `flight_crew` (
  `E_ID` int NOT NULL,
  `F_ID` int NOT NULL,
  `Duty` varchar(45) NOT NULL,
  PRIMARY KEY (`E_ID`,`F_ID`),
  KEY `FK_FlightCrew_Flight_idx` (`F_ID`),
  CONSTRAINT `fk_FC_Employee` FOREIGN KEY (`E_ID`) REFERENCES `employee` (`E_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_FC_Flight` FOREIGN KEY (`F_ID`) REFERENCES `flight` (`F_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `flight_crew`
INSERT INTO `flight_crew` VALUES 
(3, 1, 'Pilot'),
(3, 4, 'Pilot'),
(3, 14, 'Pilot'),
(3, 17, 'Pilot'),
(3, 18, 'Pilot'),
(3, 19, 'Pilot'),
(3, 20, 'Pilot'),
(3, 22, 'Pilot'),
(3, 25, 'Pilot'),
(3, 26, 'Pilot'),
(3, 27, 'Pilot'),
(3, 30, 'Pilot'),
(3, 31, 'Pilot'),
(4, 2, 'Pilot'),
(4, 14, 'Pilot'),
(4, 17, 'Pilot'),
(4, 18, 'Pilot'),
(4, 19, 'Pilot'),
(4, 20, 'Pilot'),
(4, 22, 'Pilot'),
(4, 25, 'Pilot'),
(4, 26, 'Pilot'),
(4, 27, 'Pilot'),
(4, 30, 'Pilot'),
(4, 31, 'Pilot'),
(5, 2, 'Pilot'),
(5, 14, 'Pilot'),
(5, 17, 'Pilot'),
(5, 18, 'Pilot'),
(5, 19, 'Pilot'),
(5, 22, 'Pilot'),
(5, 25, 'Pilot'),
(5, 26, 'Pilot'),
(5, 31, 'Pilot'),
(6, 2, 'Pilot'),
(6, 4, 'Pilot'),
(6, 16, 'Pilot'),
(6, 21, 'Pilot'),
(6, 23, 'Pilot'),
(6, 28, 'Pilot'),
(7, 3, 'Pilot'),
(7, 4, 'Pilot'),
(7, 16, 'Pilot'),
(7, 23, 'Pilot'),
(7, 28, 'Pilot'),
(8, 1, 'Pilot'),
(8, 6, 'Pilot'),
(8, 15, 'Pilot'),
(8, 24, 'Pilot'),
(8, 29, 'Pilot'),
(9, 1, 'Pilot'),
(9, 6, 'Pilot'),
(9, 24, 'Pilot'),
(9, 29, 'Pilot'),
(10, 3, 'Pilot'),
(10, 5, 'Pilot'),
(10, 15, 'Pilot'),
(10, 23, 'Pilot'),
(11, 3, 'Pilot'),
(11, 15, 'Pilot'),
(12, 5, 'Pilot'),
(12, 16, 'Pilot'),
(12, 21, 'Pilot'),
(13, 1, 'Attendant'),
(13, 4, 'Attendant'),
(13, 14, 'Attendant'),
(13, 17, 'Attendant'),
(13, 18, 'Attendant'),
(13, 19, 'Attendant'),
(13, 20, 'Attendant'),
(13, 22, 'Attendant'),
(13, 25, 'Attendant'),
(13, 26, 'Attendant'),
(13, 27, 'Attendant'),
(13, 30, 'Attendant'),
(13, 31, 'Attendant'),
(14, 1, 'Attendant'),
(14, 4, 'Attendant'),
(14, 14, 'Attendant'),
(14, 17, 'Attendant'),
(14, 18, 'Attendant'),
(14, 19, 'Attendant'),
(14, 20, 'Attendant'),
(14, 22, 'Attendant'),
(14, 25, 'Attendant'),
(14, 26, 'Attendant'),
(14, 27, 'Attendant'),
(14, 30, 'Attendant'),
(14, 31, 'Attendant'),
(15, 4, 'Attendant'),
(15, 14, 'Attendant'),
(15, 17, 'Attendant'),
(15, 18, 'Attendant'),
(15, 19, 'Attendant'),
(15, 20, 'Attendant'),
(15, 22, 'Attendant'),
(15, 25, 'Attendant'),
(15, 26, 'Attendant'),
(15, 27, 'Attendant'),
(15, 31, 'Attendant'),
(16, 1, 'Attendant'),
(16, 6, 'Attendant'),
(16, 14, 'Attendant'),
(16, 17, 'Attendant'),
(16, 18, 'Attendant'),
(16, 22, 'Attendant'),
(16, 28, 'Attendant'),
(16, 30, 'Attendant'),
(17, 2, 'Attendant'),
(17, 4, 'Attendant'),
(17, 14, 'Attendant'),
(17, 17, 'Attendant'),
(17, 18, 'Attendant'),
(17, 19, 'Attendant'),
(17, 22, 'Attendant'),
(17, 25, 'Attendant'),
(17, 26, 'Attendant'),
(17, 31, 'Attendant'),
(18, 1, 'Attendant'),
(18, 6, 'Attendant'),
(18, 14, 'Attendant'),
(18, 17, 'Attendant'),
(18, 18, 'Attendant'),
(18, 22, 'Attendant'),
(18, 28, 'Attendant'),
(19, 2, 'Attendant'),
(19, 4, 'Attendant'),
(19, 16, 'Attendant'),
(19, 19, 'Attendant'),
(19, 23, 'Attendant'),
(19, 25, 'Attendant'),
(19, 26, 'Attendant'),
(19, 31, 'Attendant'),
(20, 1, 'Attendant'),
(20, 6, 'Attendant'),
(20, 15, 'Attendant'),
(20, 24, 'Attendant'),
(20, 28, 'Attendant'),
(21, 2, 'Attendant'),
(21, 4, 'Attendant'),
(21, 16, 'Attendant'),
(21, 19, 'Attendant'),
(21, 23, 'Attendant'),
(21, 25, 'Attendant'),
(21, 26, 'Attendant'),
(21, 31, 'Attendant'),
(22, 2, 'Attendant'),
(22, 15, 'Attendant'),
(22, 21, 'Attendant'),
(22, 23, 'Attendant'),
(23, 1, 'Attendant'),
(23, 15, 'Attendant'),
(23, 24, 'Attendant'),
(23, 29, 'Attendant'),
(24, 2, 'Attendant'),
(24, 3, 'Attendant'),
(24, 5, 'Attendant'),
(24, 16, 'Attendant'),
(24, 21, 'Attendant'),
(24, 23, 'Attendant'),
(25, 2, 'Attendant'),
(25, 3, 'Attendant'),
(25, 5, 'Attendant'),
(25, 16, 'Attendant'),
(25, 21, 'Attendant'),
(25, 23, 'Attendant'),
(26, 3, 'Attendant'),
(26, 24, 'Attendant'),
(26, 29, 'Attendant'),
(27, 3, 'Attendant'),
(27, 5, 'Attendant'),
(27, 15, 'Attendant'),
(27, 21, 'Attendant'),
(27, 23, 'Attendant'),
(28, 15, 'Attendant'),
(28, 21, 'Attendant'),
(29, 3, 'Attendant'),
(29, 29, 'Attendant'),
(30, 3, 'Attendant'),
(30, 16, 'Attendant'),
(30, 21, 'Attendant'),
(31, 15, 'Attendant'),
(32, 16, 'Attendant'),
(33, 21, 'Pilot');

-- Table structure for table `flight_ticket`
DROP TABLE IF EXISTS `flight_ticket`;
CREATE TABLE `flight_ticket` (
  `Ticket_ID` int NOT NULL AUTO_INCREMENT,
  `Status` varchar(45) DEFAULT NULL,
  `Seat_Column` varchar(45) NOT NULL,
  `Seat_Row` int NOT NULL,
  `Seat_A_ID` int NOT NULL,
  `Seat_Class_Type` varchar(45) NOT NULL,
  `F_ID` int NOT NULL,
  `B_ID` int NOT NULL,
  PRIMARY KEY (`Ticket_ID`),
  UNIQUE KEY `ticket_seat` (`F_ID`,`Seat_A_ID`,`Seat_Row`,`Seat_Column`,`Seat_Class_Type`),
  KEY `fk_ticket` (`Seat_Column`,`Seat_Row`,`Seat_A_ID`,`Seat_Class_Type`),
  KEY `fk_flight` (`F_ID`),
  KEY `fk_booking` (`B_ID`) /*!80000 INVISIBLE */,
  CONSTRAINT `fk_booking` FOREIGN KEY (`B_ID`) REFERENCES `booking` (`B_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_Flight` FOREIGN KEY (`F_ID`) REFERENCES `flight` (`F_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_Seat` FOREIGN KEY (`Seat_Column`, `Seat_Row`, `Seat_A_ID`, `Seat_Class_Type`) REFERENCES `seat` (`Column_Num`, `Row_Num`, `A_ID`, `Class_Type`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `flight_ticket`
INSERT INTO `flight_ticket` VALUES 
(1, 'Confirmed', 'A', 1, 1, 'Business', 1, 1),
(2, 'Confirmed', 'B', 1, 1, 'Business', 1, 2),
(3, 'Confirmed', 'A', 1, 2, 'Economy', 2, 3),
(4, 'Confirmed', 'B', 1, 2, 'Economy', 2, 4),
(5, 'Confirmed', 'C', 1, 1, 'Economy', 3, 5),
(6, 'Confirmed', 'D', 1, 1, 'Economy', 3, 6),
(7, 'Confirmed', 'A', 2, 2, 'Economy', 4, 7),
(8, 'Confirmed', 'B', 2, 2, 'Economy', 4, 8),
(9, 'Confirmed', 'A', 2, 1, 'Business', 1, 15),
(10, 'Confirmed', 'B', 1, 1, 'Economy', 1, 16),
(11, 'Confirmed', 'A', 1, 1, 'Economy', 1, 17),
(12, 'Confirmed', 'B', 2, 1, 'Economy', 1, 18),
(13, 'Confirmed', 'B', 2, 1, 'Business', 1, 21),
(14, 'Confirmed', 'C', 1, 1, 'Economy', 1, 22),
(15, 'Confirmed', 'C', 1, 2, 'Economy', 13, 23),
(16, 'Cancelled', 'A', 1, 1, 'Business', 16, 24),
(17, 'Cancelled', 'B', 1, 1, 'Business', 16, 25),
(18, 'Cancelled', 'A', 2, 1, 'Business', 16, 25),
(19, 'Cancelled', 'D', 1, 1, 'Economy', 16, 25),
(20, 'Cancelled', 'C', 1, 1, 'Economy', 14, 26),
(21, 'Cancelled', 'B', 2, 1, 'Economy', 16, 27),
(22, 'Confirmed', 'A', 1, 2, 'Economy', 20, 28),
(23, 'Confirmed', 'B', 1, 2, 'Economy', 20, 28),
(24, 'Confirmed', 'C', 1, 2, 'Economy', 20, 28),
(25, 'Cancelled', 'B', 1, 1, 'Business', 14, 29),
(26, 'Cancelled', 'B', 1, 1, 'Economy', 14, 29),
(27, 'Cancelled', 'A', 2, 1, 'Economy', 14, 29),
(28, 'Cancelled', 'A', 1, 1, 'Business', 17, 30),
(29, 'Cancelled', 'B', 1, 1, 'Business', 17, 30),
(30, 'Cancelled', 'C', 1, 1, 'Economy', 17, 30),
(31, 'Cancelled', 'B', 2, 1, 'Business', 17, 31),
(32, 'Cancelled', 'B', 1, 1, 'Economy', 17, 31),
(33, 'Cancelled', 'D', 1, 1, 'Economy', 17, 31),
(34, 'Confirmed', 'A', 1, 2, 'Economy', 24, 32),
(35, 'Confirmed', 'B', 1, 2, 'Economy', 24, 33),
(36, 'Confirmed', 'A', 1, 1, 'Economy', 25, 34),
(37, 'Confirmed', 'B', 1, 1, 'Economy', 25, 34),
(38, 'Confirmed', 'C', 1, 2, 'Economy', 24, 35),
(39, 'Confirmed', 'D', 1, 2, 'Economy', 24, 36),
(40, 'Confirmed', 'A', 2, 2, 'Economy', 24, 37),
(41, 'Confirmed', 'A', 1, 1, 'Economy', 22, 38),
(42, 'Confirmed', 'B', 1, 1, 'Economy', 22, 38),
(43, 'Confirmed', 'A', 1, 6, 'Economy', 29, 39),
(44, 'Confirmed', 'B', 1, 6, 'Economy', 29, 39),
(45, 'Confirmed', 'C', 1, 6, 'Economy', 29, 39),
(46, 'Cancelled', 'D', 1, 6, 'Economy', 29, 40),
(47, 'Cancelled', 'A', 2, 6, 'Economy', 29, 40),
(48, 'Cancelled', 'B', 2, 6, 'Economy', 29, 40),
(49, 'Confirmed', 'A', 1, 1, 'Economy', 17, 41),
(50, 'Confirmed', 'A', 2, 1, 'Economy', 17, 41);

-- Table structure for table `guest`
DROP TABLE IF EXISTS `guest`;
CREATE TABLE `guest` (
  `Email_G_ID` varchar(45) NOT NULL,
  PRIMARY KEY (`Email_G_ID`),
  UNIQUE KEY `Email_G_ID_UNIQUE` (`Email_G_ID`),
  CONSTRAINT `fk_Guest_Client` FOREIGN KEY (`Email_G_ID`) REFERENCES `client` (`Email_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `guest`
INSERT INTO `guest` VALUES 
('guest1@example.com'),
('guest2@example.com'),
('guest@mail'),
('inbal@mon'),
('osher@melich'),
('yonatan@hakatan');

-- Table structure for table `manger`
DROP TABLE IF EXISTS `manger`;
CREATE TABLE `manger` (
  `E_ID` int NOT NULL,
  `Password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`E_ID`),
  CONSTRAINT `FK_Manger` FOREIGN KEY (`E_ID`) REFERENCES `employee` (`E_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `manger`
INSERT INTO `manger` VALUES 
(1, 'admin123'),
(2, 'boss456');

-- Table structure for table `pilot`
DROP TABLE IF EXISTS `pilot`;
CREATE TABLE `pilot` (
  `E_ID` int NOT NULL,
  `Training_for_long_flights` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`E_ID`),
  CONSTRAINT `FK_Pilot_Employee` FOREIGN KEY (`E_ID`) REFERENCES `employee` (`E_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `pilot`
INSERT INTO `pilot` VALUES 
(3, 'Yes'),
(4, 'Yes'),
(5, 'Yes'),
(6, 'Yes'),
(7, 'Yes'),
(8, 'No'),
(9, 'No'),
(10, 'Yes'),
(11, 'No'),
(12, 'Yes'),
(33, 'Yes');

-- Table structure for table `registered`
DROP TABLE IF EXISTS `registered`;
CREATE TABLE `registered` (
  `Email_R_ID` varchar(45) NOT NULL,
  `Registration_date` datetime DEFAULT NULL,
  `Date_of_birth` datetime DEFAULT NULL,
  `Passport_number` varchar(45) DEFAULT NULL,
  `First_Name` varchar(45) DEFAULT NULL,
  `Last_Name` varchar(45) DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Email_R_ID`),
  UNIQUE KEY `Email_R_ID_UNIQUE` (`Email_R_ID`),
  CONSTRAINT `fk_Registered_Client` FOREIGN KEY (`Email_R_ID`) REFERENCES `client` (`Email_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `registered`
INSERT INTO `registered` VALUES 
('elad@bensh', '2026-01-20 00:00:00', '2026-01-01 00:00:00', '987654321', 'Elad', 'Ben', '123456'),
('monkey@luffy', '2026-01-20 00:00:00', '2025-02-04 00:00:00', '147852369', 'monkey', 'd. luffy', '123456'),
('reg1@flytau.com', '2023-01-01 00:00:00', '1990-05-10 00:00:00', '123456789', 'Lior', 'Ben_David', 'reg1pass'),
('reg2@flytau.com', '2023-02-15 00:00:00', '1988-11-20 00:00:00', '987654321', 'Shani', 'Gold', 'reg2pass'),
('shir@lev', '2026-01-20 00:00:00', '2026-01-01 00:00:00', '123456', 'Shir', 'Lev', '1234'),
('shiralevy2017@gmail.com', '2025-12-26 00:00:00', '1999-07-14 00:00:00', '123456', 'Shira', 'Levy', '12345678'),
('shmulik@cohen', '2026-01-20 00:00:00', '2017-02-15 00:00:00', '123456', 'shmulik', 'cohen', '1234');

-- Table structure for table `registered_phone`
DROP TABLE IF EXISTS `registered_phone`;
CREATE TABLE `registered_phone` (
  `Email_R_ID` varchar(255) NOT NULL,
  `Phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`Email_R_ID`,`Phone_number`),
  CONSTRAINT `registered_phone_ibfk_1` FOREIGN KEY (`Email_R_ID`) REFERENCES `registered` (`Email_R_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `registered_phone`
INSERT INTO `registered_phone` VALUES 
('monkey@luffy', '05011111111'),
('monkey@luffy', '05022222222'),
('monkey@luffy', '0503333333'),
('monkey@luffy', '05044444444'),
('monkey@luffy', '05055555555'),
('reg1@flytau.com', '972505551111'),
('reg2@flytau.com', '972505552222'),
('shiralevy2017@gmail.com', '0584662727'),
('shmulik@cohen', '050111111'),
('shmulik@cohen', '0502222222'),
('shmulik@cohen', '050333333');

-- Table structure for table `route`
DROP TABLE IF EXISTS `route`;
CREATE TABLE `route` (
  `R_ID` int NOT NULL,
  `Airport_Name_Source` varchar(45) NOT NULL,
  `Airport_Name_Dest` varchar(45) NOT NULL,
  `Flight_Duration` int DEFAULT NULL,
  PRIMARY KEY (`R_ID`),
  KEY `FK_Route_Source_idx` (`Airport_Name_Source`),
  KEY `FK_Route_Destniation_idx` (`Airport_Name_Dest`),
  CONSTRAINT `FK_Destniation` FOREIGN KEY (`Airport_Name_Dest`) REFERENCES `airport` (`Airport_Name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_Source` FOREIGN KEY (`Airport_Name_Source`) REFERENCES `airport` (`Airport_Name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `route`
INSERT INTO `route` VALUES 
(1, 'Ben Gurion', 'Heathrow', 5),
(2, 'Ben Gurion', 'JFK', 11),
(3, 'Heathrow', 'Ben Gurion', 4),
(4, 'Ben Gurion', 'Schiphol', 7),
(5, 'Ben Gurion', 'Charles de Gaulle', 8),
(6, 'JFK', 'Heathrow', 7),
(7, 'Heathrow', 'JFK', 8),
(8, 'JFK', 'Los Angeles Int', 6),
(9, 'Los Angeles Int', 'JFK', 5),
(10, 'Dubai Int', 'Ben Gurion', 3),
(11, 'Ben Gurion', 'Dubai Int', 3),
(12, 'Tokyo Haneda', 'Sydney Kingsford', 9),
(13, 'Sydney Kingsford', 'Tokyo Haneda', 10),
(14, 'Charles de Gaulle', 'Toronto Pearson', 8),
(15, 'Toronto Pearson', 'Charles de Gaulle', 7);

-- Table structure for table `seat`
DROP TABLE IF EXISTS `seat`;
CREATE TABLE `seat` (
  `Column_Num` varchar(45) NOT NULL,
  `Row_Num` int NOT NULL,
  `A_ID` int NOT NULL,
  `Class_Type` varchar(45) NOT NULL,
  PRIMARY KEY (`Column_Num`,`Row_Num`,`A_ID`,`Class_Type`),
  KEY `fk_Seat_Class1_idx` (`A_ID`,`Class_Type`),
  CONSTRAINT `fk_Seat_Class1` FOREIGN KEY (`A_ID`, `Class_Type`) REFERENCES `class` (`A_ID`, `Type`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table `seat`
INSERT INTO `seat` VALUES 
('A', 1, 1, 'Business'),
('A', 2, 1, 'Business'),
('B', 1, 1, 'Business'),
('B', 2, 1, 'Business'),
('A', 1, 1, 'Economy'),
('A', 2, 1, 'Economy'),
('B', 1, 1, 'Economy'),
('B', 2, 1, 'Economy'),
('C', 1, 1, 'Economy'),
('C', 2, 1, 'Economy'),
('D', 1, 1, 'Economy'),
('D', 2, 1, 'Economy'),
('A', 1, 2, 'Economy'),
('A', 2, 2, 'Economy'),
('B', 1, 2, 'Economy'),
('B', 2, 2, 'Economy'),
('C', 1, 2, 'Economy'),
('C', 2, 2, 'Economy'),
('D', 1, 2, 'Economy'),
('D', 2, 2, 'Economy'),
('A', 1, 3, 'Economy'),
('A', 2, 3, 'Economy'),
('B', 1, 3, 'Economy'),
('B', 2, 3, 'Economy'),
('C', 1, 3, 'Economy'),
('C', 2, 3, 'Economy'),
('D', 1, 3, 'Economy'),
('D', 2, 3, 'Economy'),
('A', 1, 4, 'Business'),
('A', 2, 4, 'Business'),
('B', 1, 4, 'Business'),
('B', 2, 4, 'Business'),
('A', 1, 4, 'Economy'),
('A', 2, 4, 'Economy'),
('B', 1, 4, 'Economy'),
('B', 2, 4, 'Economy'),
('C', 1, 4, 'Economy'),
('C', 2, 4, 'Economy'),
('D', 1, 4, 'Economy'),
('D', 2, 4, 'Economy'),
('A', 1, 5, 'Economy'),
('A', 2, 5, 'Economy'),
('B', 1, 5, 'Economy'),
('B', 2, 5, 'Economy'),
('C', 1, 5, 'Economy'),
('C', 2, 5, 'Economy'),
('D', 1, 5, 'Economy'),
('D', 2, 5, 'Economy'),
('A', 1, 6, 'Economy'),
('A', 2, 6, 'Economy'),
('B', 1, 6, 'Economy'),
('B', 2, 6, 'Economy'),
('C', 1, 6, 'Economy'),
('C', 2, 6, 'Economy'),
('D', 1, 6, 'Economy'),
('D', 2, 6, 'Economy');

SET FOREIGN_KEY_CHECKS=1;
