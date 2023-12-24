-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 23 Des 2023 pada 16.34
-- Versi server: 10.4.14-MariaDB
-- Versi PHP: 7.2.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sentimen_ta`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tes_model`
--

CREATE TABLE `tes_model` (
  `id` int(11) NOT NULL,
  `Tweet` text DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `tes` enum('false','true') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tes_model`
--

INSERT INTO `tes_model` (`id`, `Tweet`, `label`, `tes`) VALUES
(1, 'pssi semakin maju', 'positif', 'true'),
(2, 'pssi sangat buruk sekali', 'netral', 'true'),
(3, 'pssi semakin ddepan', 'netral', 'true');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('user','admin') DEFAULT NULL,
  `password` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id_user`, `username`, `email`, `role`, `password`) VALUES
(1, 'Fikri1', 'fikri1@gmail.com', 'admin', 'pbkdf2:sha256:600000$ubnlmE9I3oxETGwx$b89512f69a144e9e02af1d69449e186f4c78f97bcdb6bf0d541708ef6ca3e7b1'),
(6, 'admin-pssi', 'adminpssi@gmail.com', 'admin', 'pbkdf2:sha256:600000$AKCidZrBsoXAuicH$9d0f6d179410ebd9f733632030043d44807a087dee179efc5409deef1bbbf6d4'),
(7, 'user-pssi', 'user-pssi@gmail.com', 'user', 'pbkdf2:sha256:600000$Z0PTqNzL1wTQE3Cp$53f15bcbfa0568032e8209ac7ca2952623e474ddcf8b897152c81cc9129121fb'),
(8, 'fikri', 'fikri@gmail.com', 'user', 'pbkdf2:sha256:600000$RphaoOBvfePAdWxc$540d18314b16f1b8a38a17487259bba2d99c214e8fe4cad8959e8143d1d58fb5'),
(10, 'user-fikri', 'userfikri123@gmail.com', 'user', 'pbkdf2:sha256:600000$g34nImBNzbBOVv0B$1e17e8af48d05f8d70193e15de6521f377f381af87eb11c53349d24191584260');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tes_model`
--
ALTER TABLE `tes_model`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `tes_model`
--
ALTER TABLE `tes_model`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
