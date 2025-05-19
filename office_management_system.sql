-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: May 08, 2025 at 05:58 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `office_management_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `EmpNo` int(11) NOT NULL,
  `Date` date NOT NULL,
  `Status` enum('Present','Absent','Leave') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`EmpNo`, `Date`, `Status`) VALUES
(1, '2023-10-01', 'Present'),
(1, '2023-10-02', 'Present'),
(1, '2023-10-03', 'Leave'),
(1, '2023-10-04', 'Present'),
(2, '2023-10-01', 'Present'),
(2, '2023-10-02', 'Absent'),
(2, '2023-10-03', 'Present'),
(2, '2023-10-04', 'Present'),
(3, '2023-10-01', 'Present'),
(3, '2023-10-02', 'Present'),
(3, '2023-10-03', 'Present'),
(3, '2023-10-04', 'Leave');

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `DeptID` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`DeptID`, `name`, `area`) VALUES
(1, 'Software', 'Pechs'),
(2, 'Hardware', 'Saddar'),
(3, 'Electronics', 'Jouhar'),
(4, 'Electrical', 'Cantt');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `EmpNo` int(11) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `phone_number` varchar(14) DEFAULT NULL,
  `Department_ID` int(11) DEFAULT NULL,
  `manager_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`EmpNo`, `name`, `address`, `phone_number`, `Department_ID`, `manager_id`) VALUES
(1, 'Ali Khan', 'House 45, Street 10, F-8/3, Islamabad', '+923001234567', 1, NULL),
(2, 'Fatima Ahmed', 'Flat 301, Garden Heights, Main Clifton Road, Karachi', '+923217654321', 2, 1),
(3, 'Usman Malik', '14 Commercial Area, DHA Phase 5, Lahore', '+923339876543', 3, 2),
(4, 'Ayesha Raza', 'Plot 67, Sector H-9, Bahria Town, Rawalpindi', '+923452345678', 4, 2),
(5, 'Bilal Hassan', 'Shop 5, Saddar Bazaar, Peshawar Cantt', '+923113456789', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `salary`
--

CREATE TABLE `salary` (
  `EmpNo` int(11) NOT NULL,
  `SalaryType` enum('Fixed','PerDay') DEFAULT NULL,
  `FixedSalary` decimal(10,2) DEFAULT NULL,
  `PerDayRate` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salary`
--

INSERT INTO `salary` (`EmpNo`, `SalaryType`, `FixedSalary`, `PerDayRate`) VALUES
(1, 'Fixed', 120000.00, NULL),
(2, 'Fixed', 85000.00, NULL),
(3, 'Fixed', 75000.00, NULL),
(4, 'PerDay', NULL, 3000.00),
(5, 'PerDay', NULL, 2500.00);

-- --------------------------------------------------------

--
-- Table structure for table `salary_history`
--

CREATE TABLE `salary_history` (
  `HistoryID` int(11) NOT NULL,
  `EmpNo` int(11) DEFAULT NULL,
  `TotalSalary` decimal(10,2) DEFAULT NULL,
  `MonthYear` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salary_history`
--

INSERT INTO `salary_history` (`HistoryID`, `EmpNo`, `TotalSalary`, `MonthYear`) VALUES
(1, 1, 120000.00, '2023-09-30'),
(2, 2, 85000.00, '2023-09-30'),
(3, 3, 75000.00, '2023-09-30'),
(4, 4, 72000.00, '2023-09-30'),
(5, 5, 55000.00, '2023-09-30'),
(6, 1, 120000.00, '2023-08-31'),
(7, 2, 85000.00, '2023-08-31'),
(8, 3, 75000.00, '2023-08-31'),
(9, 4, 69000.00, '2023-08-31'),
(10, 5, 50000.00, '2023-08-31');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`EmpNo`,`Date`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`DeptID`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`EmpNo`),
  ADD KEY `Department_ID` (`Department_ID`),
  ADD KEY `fk_manager` (`manager_id`);

--
-- Indexes for table `salary`
--
ALTER TABLE `salary`
  ADD PRIMARY KEY (`EmpNo`);

--
-- Indexes for table `salary_history`
--
ALTER TABLE `salary_history`
  ADD PRIMARY KEY (`HistoryID`),
  ADD KEY `EmpNo` (`EmpNo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `EmpNo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `salary_history`
--
ALTER TABLE `salary_history`
  MODIFY `HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`EmpNo`) REFERENCES `employee` (`EmpNo`);

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`Department_ID`) REFERENCES `department` (`DeptID`),
  ADD CONSTRAINT `fk_manager` FOREIGN KEY (`manager_id`) REFERENCES `employee` (`EmpNo`) ON DELETE SET NULL;

--
-- Constraints for table `salary`
--
ALTER TABLE `salary`
  ADD CONSTRAINT `salary_ibfk_1` FOREIGN KEY (`EmpNo`) REFERENCES `employee` (`EmpNo`);

--
-- Constraints for table `salary_history`
--
ALTER TABLE `salary_history`
  ADD CONSTRAINT `salary_history_ibfk_1` FOREIGN KEY (`EmpNo`) REFERENCES `employee` (`EmpNo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
