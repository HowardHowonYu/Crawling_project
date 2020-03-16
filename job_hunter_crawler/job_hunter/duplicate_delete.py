import MySQLdb.cursors

def duplicate_delete():
    # MySQL Connection 연결
    conn = MySQLdb.connect(user='root', passwd='dss', db='job_hunter', host='15.164.136.109', charset="utf8", use_unicode=True)
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    
    # SQL문 실행
    sql = "delete from job_hunter where id not in (select * from (select min(id) from job_hunter group by link, position) as temp);"
    curs.execute(sql)
    conn.commit()
    # # 데이타 Fetch
    # rows = curs.fetchall()
    # print(rows)     # 전체 rows
    # # print(rows[0])  # 첫번째 row: (1, '김정수', 1, '서울')
    # # print(rows[1])  # 두번째 row: (2, '강수정', 2, '서울')
    
    # # Connection 닫기
    conn.close()

duplicate_delete()