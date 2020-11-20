-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 20 nov. 2020 à 14:06
-- Version du serveur :  10.4.14-MariaDB
-- Version de PHP : 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `kasino`
--

-- --------------------------------------------------------

--
-- Structure de la table `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `player_id` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `nb_try` int(11) DEFAULT NULL,
  `bet` int(11) DEFAULT NULL,
  `gain` int(11) DEFAULT NULL,
  `played_at` timestamp NOT NULL DEFAULT current_timestamp()
) ;

--
-- Déchargement des données de la table `history`
--

INSERT INTO `history` (`id`, `player_id`, `level`, `nb_try`, `bet`, `gain`, `played_at`) VALUES
(1, 1, 1, 1, 5, 15, '2020-11-19 15:52:12'),
(2, 1, 2, 3, 12, 21, '2020-11-19 15:52:56'),
(3, 1, 3, 4, 4, 22, '2020-11-19 15:53:08'),
(4, 1, 1, 3, 4, 12, '2020-11-19 17:01:29'),
(5, 1, 1, 1, 11, 23, '2020-11-20 09:27:50'),
(6, 1, 2, 3, 18, 32, '2020-11-20 09:28:15'),
(7, 1, 3, 5, 30, 40, '2020-11-20 09:29:07'),
(8, 1, 1, 1, 32, 72, '2020-11-20 09:31:44'),
(9, 1, 2, 2, 50, 72, '2020-11-20 09:31:54'),
(10, 1, 3, 2, 2, 10, '2020-11-20 10:48:13'),
(11, 1, 3, 2, 2, 10, '2020-11-20 11:03:14'),
(12, 1, 3, 2, 2, 10, '2020-11-20 11:09:40');

-- --------------------------------------------------------

--
-- Structure de la table `player`
--

CREATE TABLE `player` (
  `id` int(11) NOT NULL,
  `username` varchar(200) NOT NULL,
  `level` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ;

--
-- Déchargement des données de la table `player`
--

INSERT INTO `player` (`id`, `username`, `level`, `created_at`) VALUES
(1, 'Alex', 1, '2020-11-19 15:43:44'),
(18, '12', 1, '2020-11-20 08:57:16'),
(24, '', 1, '2020-11-20 09:26:54');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `par_ind` (`player_id`);

--
-- Index pour la table `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_username` (`username`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `player`
--
ALTER TABLE `player`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT `history_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
