-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: erp
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `erp`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `erp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `erp`;

--
-- Table structure for table `anos`
--

DROP TABLE IF EXISTS `anos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anos` (
  `id_ano` int NOT NULL AUTO_INCREMENT,
  `ano` int NOT NULL,
  PRIMARY KEY (`id_ano`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anos`
--

LOCK TABLES `anos` WRITE;
/*!40000 ALTER TABLE `anos` DISABLE KEYS */;
INSERT INTO `anos` VALUES (1,2020),(2,2021),(3,2022),(4,2023),(5,2024),(6,2025),(7,2026),(8,2027),(9,2028);
/*!40000 ALTER TABLE `anos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) DEFAULT NULL,
  `cpf_cnpj` bigint DEFAULT NULL,
  `telefone_celular` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs_atividades`
--

DROP TABLE IF EXISTS `logs_atividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_atividades` (
  `id_log` int NOT NULL AUTO_INCREMENT,
  `data_log` date NOT NULL DEFAULT (curdate()),
  `horario_log` time NOT NULL DEFAULT (curtime()),
  `usuario_log` varchar(25) NOT NULL,
  `tipo_log` varchar(100) NOT NULL,
  `conteudo_log` text NOT NULL,
  PRIMARY KEY (`id_log`),
  KEY `fk_logs_atividades_usuarios` (`usuario_log`),
  CONSTRAINT `fk_logs_atividades_usuarios` FOREIGN KEY (`usuario_log`) REFERENCES `usuarios` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_atividades`
--

LOCK TABLES `logs_atividades` WRITE;
/*!40000 ALTER TABLE `logs_atividades` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs_atividades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marcas`
--

DROP TABLE IF EXISTS `marcas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marcas` (
  `id_marca` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `pais_origem` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_marca`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marcas`
--

LOCK TABLES `marcas` WRITE;
/*!40000 ALTER TABLE `marcas` DISABLE KEYS */;
INSERT INTO `marcas` VALUES (1,'Toyota','Japão'),(2,'Ford','Estados Unidos'),(3,'Ferrari','Itália'),(4,'Saab','Suécia'),(5,'Chevrolet','Estados Unidos'),(6,'FIAT','Itália'),(7,'Hyundai','Coréia do Sul'),(8,'Citroen','França'),(9,'Renault','França'),(10,'Wolkswagen','Alemanha'),(11,'Porsche','Alemanha');
/*!40000 ALTER TABLE `marcas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meses`
--

DROP TABLE IF EXISTS `meses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meses` (
  `id_mes` int NOT NULL AUTO_INCREMENT,
  `numero_mes` tinyint NOT NULL,
  `nome_mes` varchar(20) NOT NULL,
  `abreviacao` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id_mes`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meses`
--

LOCK TABLES `meses` WRITE;
/*!40000 ALTER TABLE `meses` DISABLE KEYS */;
INSERT INTO `meses` VALUES (1,1,'Janeiro','Jan'),(2,2,'Fevereiro','Fev'),(3,3,'Março','Mar'),(4,4,'Abril','Abr'),(5,5,'Maio','Mai'),(6,6,'Junho','Jun'),(7,7,'Julho','Jul'),(8,8,'Agosto','Ago'),(9,9,'Setembro','Set'),(10,10,'Outubro','Out'),(11,11,'Novembro','Nov'),(12,12,'Dezembro','Dez');
/*!40000 ALTER TABLE `meses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordem_servico_pecas`
--

DROP TABLE IF EXISTS `ordem_servico_pecas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordem_servico_pecas` (
  `id_os_peca` int NOT NULL AUTO_INCREMENT,
  `ordem_servico_id` int DEFAULT NULL,
  `peca_id` int DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  PRIMARY KEY (`id_os_peca`),
  KEY `ordem_servico_id` (`ordem_servico_id`),
  KEY `peca_id` (`peca_id`),
  CONSTRAINT `ordem_servico_pecas_ibfk_1` FOREIGN KEY (`ordem_servico_id`) REFERENCES `ordens_servico` (`id_ordem_servico`),
  CONSTRAINT `ordem_servico_pecas_ibfk_2` FOREIGN KEY (`peca_id`) REFERENCES `pecas` (`id_peca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordem_servico_pecas`
--

LOCK TABLES `ordem_servico_pecas` WRITE;
/*!40000 ALTER TABLE `ordem_servico_pecas` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordem_servico_pecas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordem_servico_servicos`
--

DROP TABLE IF EXISTS `ordem_servico_servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordem_servico_servicos` (
  `id_os_servico` int NOT NULL AUTO_INCREMENT,
  `ordem_servico_id` int DEFAULT NULL,
  `servico_id` int DEFAULT NULL,
  PRIMARY KEY (`id_os_servico`),
  KEY `ordem_servico_id` (`ordem_servico_id`),
  KEY `servico_id` (`servico_id`),
  CONSTRAINT `ordem_servico_servicos_ibfk_1` FOREIGN KEY (`ordem_servico_id`) REFERENCES `ordens_servico` (`id_ordem_servico`),
  CONSTRAINT `ordem_servico_servicos_ibfk_2` FOREIGN KEY (`servico_id`) REFERENCES `servicos` (`id_servico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordem_servico_servicos`
--

LOCK TABLES `ordem_servico_servicos` WRITE;
/*!40000 ALTER TABLE `ordem_servico_servicos` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordem_servico_servicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordens_servico`
--

DROP TABLE IF EXISTS `ordens_servico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordens_servico` (
  `id_ordem_servico` int NOT NULL AUTO_INCREMENT,
  `veiculo_id` int DEFAULT NULL,
  `data` date DEFAULT NULL,
  `observacoes` text,
  PRIMARY KEY (`id_ordem_servico`),
  KEY `carro_id` (`veiculo_id`),
  CONSTRAINT `ordens_servico_ibfk_1` FOREIGN KEY (`veiculo_id`) REFERENCES `veiculos` (`id_veiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordens_servico`
--

LOCK TABLES `ordens_servico` WRITE;
/*!40000 ALTER TABLE `ordens_servico` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordens_servico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pecas`
--

DROP TABLE IF EXISTS `pecas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pecas` (
  `id_peca` int NOT NULL AUTO_INCREMENT,
  `descricao` varchar(100) DEFAULT NULL,
  `preco` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_peca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pecas`
--

LOCK TABLES `pecas` WRITE;
/*!40000 ALTER TABLE `pecas` DISABLE KEYS */;
/*!40000 ALTER TABLE `pecas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `id_produto` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) DEFAULT NULL,
  `preco` decimal(10,2) DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  PRIMARY KEY (`id_produto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicos`
--

DROP TABLE IF EXISTS `servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicos` (
  `id_servico` int NOT NULL AUTO_INCREMENT,
  `descricao` varchar(100) DEFAULT NULL,
  `preco` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_servico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos`
--

LOCK TABLES `servicos` WRITE;
/*!40000 ALTER TABLE `servicos` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `login` varchar(25) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cpf` bigint NOT NULL,
  `telefone` varchar(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `sexo` char(1) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `chave_usuario` (`login`,`senha`),
  UNIQUE KEY `unq_usuarios_nome` (`nome`,`cpf`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `veiculos`
--

DROP TABLE IF EXISTS `veiculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `veiculos` (
  `id_veiculo` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int DEFAULT NULL,
  `placa` varchar(10) DEFAULT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `ano` int DEFAULT NULL,
  PRIMARY KEY (`id_veiculo`),
  UNIQUE KEY `placa` (`placa`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `veiculos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veiculos`
--

LOCK TABLES `veiculos` WRITE;
/*!40000 ALTER TABLE `veiculos` DISABLE KEYS */;
/*!40000 ALTER TABLE `veiculos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-18 13:10:16
