from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
#BLOB 읽기용
from base64 import b64encode # byte배열을 base64로 변경함.
import pandas as pd
from .models import Table2 # 해당 모델에 직접 연결, SQL 안써도 되게끔
from .models import Table1

cursor = connection.cursor()

def dataframe(request):
    if request.method=='GET':
        df = pd.read_sql(
            """
            SELECT NO, WRITER, HIT, REGDATE
            FROM BOARD_TABLE1
            """, con=connection)
        print(type(df))
        print(df["HIT"])
        print(df)
        return  render(request, 'board/dataframe.html', {"df":df.to_html(classes="table")})


@csrf_exempt
def write(request):
    if request.method=='GET':
        return render(request, 'board/write.html')
    if request.method=='POST':
        tmp =None
        if 'img' in request.FILES:
            img = request.FILES['img']
            tmp = img.read()

        ar = [
            request.POST['title'],
            request.POST['content'],
            request.POST['writer'],
            tmp
            # img.read() # 이미지를 byte[]로 변경
        ]
        # print(ar)

        try:
            sql="""
                INSERT INTO BOARD_TABLE1(TITLE, CONTENT, WRITER, IMG, HIT, REGDATE)
                VALUES(%s, %s, %s, %s, 0, SYSDATE)
            """
            cursor.execute(sql, ar)
        except Exception as e:
            print(e)
        return redirect("/board/list")

@csrf_exempt
def list(request):
    if request.method=='GET':
        option = request.GET.get('search_option', None) # title, content, writer
        search = request.GET.get('search_text', None)

        request.session['hit'] = 1 # 세션에  hit=1
        writer = request.GET.get('writer', None)

        page = int(request.GET.get("page", 1))
        page_end = page*10 + 1
        page_start = page_end-10
        print (option == "title")

        if option == "title":
            sql1 = "SELECT NO, TITLE, WRITER, HIT, REGDATE,  ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN FROM BOARD_TABLE1 WHERE TITLE LIKE \'%" + str(search) + "%\'"
            sql2 = "SELECT * FROM (" + sql1 + ") WHERE ROWN BETWEEN " + str(page_start) + " and " + str(page_end)         # WHERE TITLE LIKE '%1%'
            print(sql2)
            sqlc = "SELECT COUNT(*) FROM (" + sql1 + ")"
            cursor.execute(sqlc)
            cnt = cursor.fetchone()[0]
            tot = (cnt-1)//10+1
            
            cursor.execute(sql2)
        elif option == "content":
            sql1 = "SELECT NO, TITLE, WRITER, HIT, REGDATE,  ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN FROM BOARD_TABLE1 WHERE CONTENT LIKE \'%%" + str(search) + "%%\'"
            sql2 = "SELECT * FROM (" + sql1 + ") WHERE ROWN BETWEEN " + str(page_start) + " and " + str(page_end)

            sqlc = "SELECT COUNT(*) FROM (" + sql1 + ")"
            cursor.execute(sqlc)
            cnt = cursor.fetchone()[0]
            tot = (cnt-1)//10+1
            
            cursor.execute(sql2)
        elif option == "writer":
            sql1 = "SELECT NO, TITLE, WRITER, HIT, REGDATE,  ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN FROM BOARD_TABLE1 WHERE WRITER LIKE \'%%" + str(search) + "%%\'"
            sql2 = "SELECT * FROM (" + sql1 + ") WHERE ROWN BETWEEN " + str(page_start) + " and " + str(page_end)

            sqlc = "SELECT COUNT(*) FROM (" + sql1 + ")"
            cursor.execute(sqlc)
            cnt = cursor.fetchone()[0]
            tot = (cnt-1)//10+1
            
            cursor.execute(sql2)
        else: 

            if writer != None:
                sql1 = "SELECT NO, TITLE, WRITER, HIT, REGDATE,  ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN FROM BOARD_TABLE1 WHERE WRITER=%s"
                sql2 = "SELECT * FROM (" + sql1 + ") WHERE ROWN BETWEEN " + str(page_start) + " and " + str(page_end)

                sqlc = "SELECT COUNT(*) FROM (" + sql1 + ")"
                cursor.execute(sqlc, [writer])
                cnt = cursor.fetchone()[0]
                tot = (cnt-1)//10+1

                # sql = """
                #     SELECT NO, TITLE, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS') 
                #     FROM BOARD_TABLE1
                #     WHERE WRITER=%s
                #     ORDER BY NO DESC
                # """
                cursor.execute(sql2,[writer])
            else:    
                sql1 = "SELECT NO, TITLE, WRITER, HIT, REGDATE,  ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN FROM BOARD_TABLE1"
                sql2 = "SELECT * FROM (" + sql1 + ") WHERE ROWN BETWEEN " + str(page_start) + " and " + str(page_end)
                
                sqlc = "SELECT COUNT(*) FROM BOARD_TABLE1"
                cursor.execute(sqlc)
                cnt = cursor.fetchone()[0]
                # model .ver
                # cnt = Table1.objects.all().count() 

                tot = (cnt-1)//10+1
                # sql = """
                #     SELECT NO, TITLE, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS') 
                #     FROM BOARD_TABLE1
                #     ORDER BY NO DESC
                # """
                cursor.execute(sql2)

        data = cursor.fetchall()
        
        return render(request, 'board/list.html', {"list":data, "writer":writer, "pages": range(1, tot+1)})


# http://127.0.0.1:8000/board/content?no=13     -> 정상 작동
# http://127.0.0.1:8000/board/content           -> 에러 발생, no=0으로 되게 default값을 잡아주는 것이 좋다.
#                                               -> no = request.GET.get('no', 0) -> default 값을 0으로 줘라!
@csrf_exempt
def content(request):
    if request.method=="GET":
        no = request.GET.get('no', 0)
        if no == 0:
            return redirect( "/board/list" )

        

        # 조회수 1증가 
        #       => 새로고침하면 안늘어나게 해야 함 - 세션을 통해 컨트롤
        if request.session['hit'] == 1:
            sql = """
                UPDATE BOARD_TABLE1 
                SET HIT=HIT+1
                WHERE no=%s
            """
            cursor.execute(sql, [no])
            request.session['hit'] = 0

        # 이전 글 번호
        sqlp = """
            SELECT NVL(max(no),0)
            FROM board_table1 
            where no<%s
        """
        cursor.execute(sqlp, [no])
        prev = cursor.fetchone()
        # 이전 글 없을 때 if로 처리
        # if prev[0] == 0:
        #     prev = (no,)

        # 다음 글 번호
        sqln = """
            SELECT NVL(min(no),0)
            FROM board_table1 
            where no>%s
        """
        cursor.execute(sqln, [no])
        nxt = cursor.fetchone()
        # 다음 글 없을 때 if로 처리
        # if nxt[0] == 0:
        #     nxt = (no,)

        # 작성자 누르면 작성자 기준 검색
        sqlsearch = """
            SELECT NO, TITLE, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS'), IMG 
            FROM BOARD_TABLE1
            WHERE NO=%s
        """
 
        # 가져오기
        sql = """
            SELECT NO, TITLE, CONTENT, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS'), IMG 
            FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()
        print(data) 

        if data[6]:
            img = data[6].read() # 바이트 배열을 img에 넣음
            img64 = b64encode(img).decode("utf-8")
        else:
            file = open('./static/img/default.png', 'rb')
            img = file.read()
            img64 = b64encode(img).decode("utf-8")

        return render(request, 'board/content.html', {"one":data, "image":img64, "prev":prev[0], "next":nxt[0]})
        
@csrf_exempt
def edit(request):
    if request.method=="GET":
        no = request.GET.get('no', 0)
        if no == 0:
            return redirect("/board/list")

        sql = """
            SELECT NO, TITLE, CONTENT, WRITER
            FROM BOARD_TABLE1
            WHERE no=%s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()

        return render(request, 'board/edit.html', {"one":data})
    if request.method=="POST":
        ar = [
            request.POST['title'], 
            request.POST['content'], 
            request.POST['writer'],
            request.POST['no']
        ]

        sql ="""
            UPDATE BOARD_TABLE1 
            SET TITLE=%s, CONTENT=%s, WRITER=%s
            WHERE NO=%s 
        """
        cursor.execute(sql, ar)
        return redirect("/board/content?no="+request.POST['no'])

# 127.0.0.1:8000/board/delete?no=37
# 127.0.0.1:8000/board/delete
@csrf_exempt  
def delete(request):
    if request.method == 'GET':   
        # request.GET.get("no", 1)     
        no = request.GET.get("no", 0)
        sql = """
            DELETE FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        return redirect("/board/list")

@csrf_exempt
def t2_insert(request):
    if request.method == "GET":
        return render(request, 'board/t2_insert.html')
    if request.method == "POST":
        obj = Table2() # obj 객체 생성
        obj.name = request.POST['name']
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.save() # 저장하기

        # ar = [
        #     request.POST['name'], 
        #     request.POST['kor'], 
        #     request.POST['eng'],
        #     request.POST['math']
        # ]
        # sql = """
        #     INSERT INTO BOARD_TABLE2 (NAME,KOR,ENG,MATH,REGDATE)
        #     VALUES (%s,%s,%s,%s,SYSDATE)
        # """
        # cursor.execute(sql, ar)
        return redirect("/board/t2_list")

# @csrf_exempt # 원래는 얘를 HTML의 form 태그 안에 {% csrf_token%}으로 해결하여야 한다.
def t2_insert_all(request):
    if request.method == "GET":
        return render(request, 'board/t2_insert_all.html', {"cnt":range(5)})
    if request.method == "POST":
        na = request.POST.getlist("name[]")
        ko = request.POST.getlist("kor[]")
        en = request.POST.getlist("eng[]")
        ma = request.POST.getlist("math[]")
        
        objs = []
        for  i in range(0, len(na)):
            obj = Table2()
            obj.name = na[i]
            obj.kor = ko[i]
            obj.eng = en[i]
            obj.math = ma[i]
            objs.append(obj)
        # save를 할 때, 일괄적으로 처리되어야 한다. 다 되거나, 하나도 안되거나
        # save 대신 사용 -> bulk_create
        Table2.objects.bulk_create(objs)

        return redirect("/board/t2_list")

@csrf_exempt
def t2_list(request):
    if request.method == "GET":
        rows = Table2.objects.all()
        # SQL : SELECT * FROM VOARD_TABLE2
        print(rows)
        print(type(rows)) # <class 'django.db.models.query.QuerySet'>
        return render(request, 'board/t2_list.html', {"list": rows})

@csrf_exempt
def t2_update(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)
        #SELECT * FROM BOARD_TABLE2 WHERE NO=%s
        row = Table2.objects.get(no=n)
        return render(request, 'board/t2_update.html',{"one":row})
    if request.method == 'POST':
        n = request.POST['no']
        obj = Table2.objects.get(no=n) #obj객체 가져옴
        obj.name = request.POST['name'] # 변수에 값
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.save() #저장하기 수행
        # UPDATE BOARD_TABLE2 SET
        # NAME=%s, KOR=%s, ENG=%s, MATH=%s
        # WHERE NO= %s
        return redirect("/board/t2_list")


def t2_update_all(request):
    if request.method == "GET":
        n = request.session['no']
        rows = Table2.objects.filter(no__in=n)
        return render(request, 'board/t2_update_all.html',{"list":rows})
    if request.method == "POST":
        menu = request.POST['menu']
        if menu=="1":
            no = request.POST.getlist("chk[]")
            request.session['no'] = no
            return redirect("/board/t2_update_all")
        if menu=="2":
            no = request.POST.getlist("no[]")
            name = request.POST.getlist("name[]")
            kor = request.POST.getlist("kor[]")
            eng = request.POST.getlist("eng[]")
            math = request.POST.getlist("math[]")

            objs = []
            for i in range(0, len(no)):
                obj = Table2.objects.get(no=no[i])
                obj.name = name[i]
                obj.kor = kor[i]
                obj.eng = eng[i]
                obj.math = math[i]
                objs.append(obj)
            Table2.objects.bulk_update(objs,["name", "kor", "eng", "math"])
            return redirect("/board/t2_list")
            

@csrf_exempt
def t2_delete(request):
    if request.method == "GET":
        n = request.GET.get("no",0)

        # SQL : SELECT * FROM BOARD_TABLE2 WHERE NO=%s
        row = Table2.objects.get(no=n)
        # SQL : DELETE * FROM BOARD_TABLE2 WHERE NO=%s
        row.delete();

        return redirect("/board/t2_list")