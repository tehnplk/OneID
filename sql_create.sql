
#drop table if exists plk_moph_id_person_check;

CREATE TABLE  IF NOT EXISTS `plk_moph_id_person_check` (
  `person_id` int(11) NOT NULL,
  `cid` varchar(13) DEFAULT NULL,
  `pname` varchar(255) DEFAULT NULL,
  `fname` varchar(255) DEFAULT NULL,
  `lname` varchar(255) DEFAULT NULL,
  `age_y` int(11) DEFAULT NULL,
  `address` varchar(255) DEFAULT '',
  `moo` varchar(255) DEFAULT NULL,
  `type_area` int(11) DEFAULT NULL,
  `moph_id_check_result` varchar(255),
  `last_check_at` datetime DEFAULT NULL,
  `last_message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`person_id`)
);

INSERT IGNORE INTO plk_moph_id_person_check  (
SELECT p.person_id,p.cid,p.pname,p.fname,p.lname,p.age_y,h.address,v.village_moo as moo,p.house_regist_type_id as type_area
,'0' as moph_id_check_result ,'2023-01-01 00:00:00' as last_check_at ,'' as last_message
FROM person p
LEFT JOIN house h on h.house_id = p.house_id
LEFT JOIN village v on v.village_id = p.village_id

WHERE p.house_regist_type_id in (1,3)
AND  p.death <> 'Y'
AND p.person_discharge_id = 9
AND p.nationality = '99'
);