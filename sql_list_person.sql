select * from plk_moph_id_person_check where moph_id_check_result = '0' and date(last_check_at) <> CURDATE()
