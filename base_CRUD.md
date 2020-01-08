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
 
-- mysql
SELECT * FROM BOARD_TABLE1 LIMIT 1,10;

-- oracle
SELECT * FROM (
    SELECT 
        NO, TITLE, CONTENT,
        ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN
    FROM
        BOARD_TABLE1)
WHERE ROWN BETWEEN 5 and 10

-- 한글이 포함된 항목 조회
SELECT * FROM BOARD_TABLE1
WHERE TITLE LIKE '%'||'김'||'%'

-- row넘버링추가하면서 SELECT 
SELECT NO, TITLE, WRITER, HIT, REGDATE,  ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN 
FROM BOARD_TABLE1 WHERE TITLE LIKE '%1%'
-- 위를 기반으로 순서대로 일부 발췌
SELECT * FROM (
    SELECT NO, TITLE, WRITER, HIT, REGDATE,  ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN 
    FROM BOARD_TABLE1 WHERE TITLE LIKE '%1%'
) WHERE ROWN BETWEEN 1 and 10
