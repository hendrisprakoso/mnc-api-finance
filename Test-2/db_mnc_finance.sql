-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 06, 2024 at 06:16 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_mnc_finance`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_accounts`
--

CREATE TABLE `tbl_accounts` (
  `user_id` varchar(36) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` mediumtext DEFAULT NULL,
  `pin` varchar(10) DEFAULT NULL,
  `token` longtext DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  `balance` bigint(20) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_accounts`
--

INSERT INTO `tbl_accounts` (`user_id`, `first_name`, `last_name`, `phone_number`, `address`, `pin`, `token`, `created_at`, `modified_at`, `balance`) VALUES
('0e0d7812-030a-4d5e-bc75-e0d71a430760', 'Tom', 'Araya', '0811255501', 'Jl. Dipnegoro No. 225', '123456', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyODEzMjE2MSwianRpIjoiMWFhOWE2N2ItZTc4ZS00YjBlLThkNDQtNTY5MTNhOWJjMDliIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjBlMGQ3ODEyLTAzMGEtNGQ1ZS1iYzc1LWUwZDcxYTQzMDc2MCIsIm5iZiI6MTcyODEzMjE2MSwiY3NyZiI6Ijg4MzUwYjIxLWNkNWUtNGFhNy05OWZkLWJkM2ZlNjc2NTU4OCIsImV4cCI6MTcyODEzMzA2MX0.DtkURZoCam7ihBI-XGyldrpq3wom1-givV7O9I756Z8', '2024-10-05 19:13:39', '2024-10-06 09:55:30', 100000),
('d1aa41ec-ee14-473d-b9c4-3453892bcc2f', 'hendri', 'prakasa', '08123123123', 'Tangerang', '12345', NULL, NULL, '2024-10-06 09:55:30', 70000);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_transactions`
--

CREATE TABLE `tbl_transactions` (
  `id` bigint(20) NOT NULL,
  `trx_code` varchar(36) NOT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `balance_before` bigint(20) DEFAULT NULL,
  `balance_after` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `account_id` varchar(36) NOT NULL,
  `trx_type` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `target_account_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_transactions`
--

INSERT INTO `tbl_transactions` (`id`, `trx_code`, `amount`, `balance_before`, `balance_after`, `created_at`, `account_id`, `trx_type`, `status`, `remarks`, `target_account_id`) VALUES
(1, '26905c62-528a-48a6-9231-4cd1cd8eb947', 50000, 100000, 150000, '2024-10-05 20:50:04', '0e0d7812-030a-4d5e-bc75-e0d71a430760', 'topup', 'success', NULL, NULL),
(2, 'bc319353-c9ad-4b23-aa5a-fe7b7d985ac2', 25000, 150000, 175000, '2024-10-05 20:56:50', '0e0d7812-030a-4d5e-bc75-e0d71a430760', 'topup', 'success', NULL, NULL),
(3, '4d32d1e5-8b9e-4c39-b910-728170c54556', 5000, 175000, 180000, '2024-10-05 20:58:01', '0e0d7812-030a-4d5e-bc75-e0d71a430760', 'topup', 'success', NULL, NULL),
(4, 'a8ae56d5-54a8-46e1-a3aa-e31fde19bd4d', 10000, 180000, 170000, '2024-10-06 08:53:38', '0e0d7812-030a-4d5e-bc75-e0d71a430760', 'payment', 'success', 'Pulsa Telkom sel 10k', NULL),
(6, '6c2d61b2-fee1-473b-aafa-7eaf43c95bdf', 10000, 130000, 120000, '2024-10-06 09:11:50', '0e0d7812-030a-4d5e-bc75-e0d71a430760', 'transfer', 'success', 'Pulsa Telkom sel 10k', 'd1aa41ec-ee14-473d-b9c4-3453892bcc2f'),
(7, 'd728a079-f45f-4fe1-bace-8e607fe74637', 10000, 120000, 110000, '2024-10-06 09:12:29', '0e0d7812-030a-4d5e-bc75-e0d71a430760', 'transfer', 'success', 'Pulsa Telkom sel 10k', 'd1aa41ec-ee14-473d-b9c4-3453892bcc2f'),
(8, '813b6abe-3913-4a0d-a1b6-df4a4d4e3d27', 10000, 110000, 100000, '2024-10-06 09:12:46', '0e0d7812-030a-4d5e-bc75-e0d71a430760', 'transfer', 'success', 'Hadiah Ulang tahun', 'd1aa41ec-ee14-473d-b9c4-3453892bcc2f');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_accounts`
--
ALTER TABLE `tbl_accounts`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `tbl_transactions`
--
ALTER TABLE `tbl_transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tbl_transactions_un` (`trx_code`),
  ADD KEY `tbl_transactions_FK` (`account_id`),
  ADD KEY `tbl_transactions_FK_1` (`target_account_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_transactions`
--
ALTER TABLE `tbl_transactions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_transactions`
--
ALTER TABLE `tbl_transactions`
  ADD CONSTRAINT `tbl_transactions_FK` FOREIGN KEY (`account_id`) REFERENCES `tbl_accounts` (`user_id`),
  ADD CONSTRAINT `tbl_transactions_FK_1` FOREIGN KEY (`target_account_id`) REFERENCES `tbl_accounts` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
