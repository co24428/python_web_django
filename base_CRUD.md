-- 추가 <br/>
INSERT INTO board_table1
    (TITLE, CONTENT, WRITER, HIT, REGDATE)
VALUES
    ('sql에서 추가', '내용', '작성자', 35, SYSDATE);  <br/>
COMMIT;

-- 삭제 (유의해라) <br/>
DELETE FROM board_table1 WHERE NO=23;

COMMIT; -- 커밋전까지는 <br/>
ROLLBACK; -- 롤백으로 되돌릴 수 있다.

-- 수정 <br/>
UPDATE board_table1 SET  TITLE='new change', CONTENT='new change content' WHERE NO=23;  <br/>
COMMIT;

-- 조회 <br/>
SELECT * FROM board_table1;  <br/>
SELECT * FROM board_table1 ORDER BY no DESC;  <br/>
SELECT * FROM board_table1 WHERE NO=23;  <br/>
SELECT * FROM board_table1 WHERE NO IN (10, 11, 12, 13, 14, 15);  <br/>
 
