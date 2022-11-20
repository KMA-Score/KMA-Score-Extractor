CREATE TABLE `Students` (
  `Id` varchar(255) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Class` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Subjects` (
  `Id` varchar(255) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `NumberOfCredits` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Scores` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `StudentId` varchar(255) DEFAULT NULL,
  `SubjectId` varchar(255) DEFAULT NULL,
  `FirstComponentScore` varchar(255) DEFAULT NULL,
  `SecondComponentScore` varchar(255) DEFAULT NULL,
  `ExamScore` varchar(255) DEFAULT NULL,
  `AvgScore` varchar(255) DEFAULT NULL,
  `AlphabetScore` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `StudentId` (`StudentId`,`SubjectId`),
  KEY `SubjectId` (`SubjectId`),
  CONSTRAINT `Scores_ibfk_1` FOREIGN KEY (`StudentId`) REFERENCES `Students` (`Id`),
  CONSTRAINT `Scores_ibfk_2` FOREIGN KEY (`SubjectId`) REFERENCES `Subjects` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT DEFAULT CHARSET=utf8mb4;