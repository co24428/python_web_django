from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#SQLite 연결
from django.db import connection
cursor = connection.cursor()

@csrf_exempt
def write(request):
    if request.method=='GET':
        return render(request, 'board/write.html')
    if request.method=='POST':
        img = request.FILES['img'] # name값 img
        ar = [
            request.POST['title'],
            request.POST['content'],
            request.POST['writer'],
            img.read() # 이미지를 byte[]로 변경
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
        request.session['hit'] = 1 # 세션에  hit=1

        sql = """
            SELECT NO, TITLE, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS') 
            FROM BOARD_TABLE1
            ORDER BY NO DESC
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        print(type(data))
        print(data)  

        return render(request, 'board/list.html', {"list":data})


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

        # 가져오기
        sql = """
            SELECT NO, TITLE, CONTENT, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS') 
            FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()

        return render(request, 'board/content.html', {"one":data})
        
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
        return redirect("/board/list")

@csrf_exempt
def delete(request):
    if request.method=="GET":
        pass