# Banco-de-Dados-N2
 
------------------------------------------------------------------------------------
MySQL Workbench Migration Wizard Report

Date: Sun Feb 28 18:08:05 2021
Source: MySQL 5.7.17
Target: MySQL 5.7.17
------------------------------------------------------------------------------------

I. Migration

1. Summary

Number of migrated schemas: 1

1. conversordb2
Source Schema:   conversordb

- Tables:             2
- Triggers:           0
- Views:              0
- Stored Procedures:  0
- Functions:          0


2. Migration Issues


3. Object Creation Issues


4. Migration Details

4.1. Table conversordb2.info_conversao (info_conversao)

Columns:
  - idConv INT(11)    
  - numConv INT(11)  NULL  
  - id_Usuario INT(11)  NULL  
  - descricao VARCHAR(45)  NULL  
  - valorObtido FLOAT  NULL  
  - convDe VARCHAR(45)  NULL  
  - convPara VARCHAR(45)  NULL  
  - resultado FLOAT  NULL  
  - dataConv DATE  NULL  

Foreign Keys:

Indices:
  - PRIMARY (idConv)


4.2. Table conversordb2.usuario (usuario)

Columns:
  - idusuario INT(11)    
  - nome VARCHAR(45)  NULL  
  - email VARCHAR(45)  NULL  
  - senha VARCHAR(45)  NULL  
  - dataCriacao DATE  NULL  

Foreign Keys:

Indices:
  - PRIMARY (idusuario)


II. Data Copy

  - `conversordb2`.`info_conversao`
            Succeeded : copied 15 of 15 rows from `conversordb`.`info_conversao`    
  - `conversordb2`.`usuario`
            Succeeded : copied 3 of 3 rows from `conversordb`.`usuario`    
