import MySQLdb.cursors

# MySQL Connection 연결
conn = MySQLdb.connect(user='root', passwd='dss', db='job_hunter', host='15.164.136.109', charset="utf8", use_unicode=True)
# Connection 으로부터 Cursor 생성
curs = conn.cursor()
conn.autocommit(True)
# SQL문 실행
# 중복 데이터 삭제
sql1 = "delete from job_hunter where id not in (select * from (select max(id) from job_hunter group by link, position) as temp);"
# id값 리셋
sql2 = "ALTER TABLE job_hunter AUTO_INCREMENT=1; SET @COUNT = 0; UPDATE job_hunter SET id = @COUNT:=@COUNT+1;"
curs.execute(sql1)
curs.execute(sql2)
