from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#DB 연결
from django.db import connection
cursor = connection.cursor()
# django에서 제공하는 User 모델 - migration하면 생성되는 것들 중 하나
from django.contrib.auth.models import User
# 미리 선언된 검증 함수들을 사용
from django.contrib.auth import login as login1
from django.contrib.auth import logout as logout1
from django.contrib.auth import authenticate as auth1

from .models import Table2
from django.db.models import Sum, Max, Min, Count, Avg 

# dataframe
import pandas as pd
# graph
import matplotlib.pyplot as plt
import io # byte로 변환
import base64 # byte배열을 base64로 변경함.
from matplotlib import font_manager, rc # 한글 폰트 적용



              
# Create your views here.
def index(request):
    # return HttpResponse("indexpagesssss")
    return render(request, 'member/index.html')

# def list(request):
#     # ID 기준으로 오름차순
#     sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
#     cursor.execute(sql)
#     data = cursor.fetchall();
#     print(type(data))
#     print(data)
    
#     # list.html을 표시하기 전에
#     # list 변수에 data값을, title변수에 "회원목록" 문자를
#     # template에서는 최대한 상수 쓰지말라. view단에서 넘기는 것이 최선의 방법 !!
#     return render(request, 'member/list.html', {"list":data, "title": "회원목록"})

@csrf_exempt  # POST로 값을 전달받는 곳은 필수로!!, 보안정책의 하나
def join(request):
    if request.method == 'GET':
        return render(request, 'member/join.html')
    if request.method == 'POST':
        id = request.POST['id']
        na = request.POST['name']
        ag = request.POST['age']
        pw = request.POST['pw']
        
        ar = [id, na, ag, pw]

        # DB에 추가
        # SQLite 버전
        # sql = """
        # INSERT INTO MEMBER(ID,NAME,AGE,PW, JOINDATE) 
        # VALUES (%s, %s, %s, %s, datetime())
        # """

        # Oracle 버전
        sql = """
        INSERT INTO MEMBER(ID,NAME,AGE,PW, JOINDATE) 
        VALUES (%s, %s, %s, %s, SYSDATE)
        """
        cursor.execute(sql,ar)

        print(ar)

        return redirect("/member/index") # 절대경로로 줘라!!, /로 시작해야 한다..

@csrf_exempt
def login(request): 
    if request.method == 'GET':
        return render(request, 'member/login.html')
    if request.method == 'POST':
        ar = [request.POST['id'], request.POST['pw']]
        sql = """
            SELECT ID, NAME 
            FROM MEMBER 
            WHERE ID=%s AND PW=%s
        """

        cursor.execute(sql, ar)
        data = cursor.fetchone() # ID가 기본키이기 때문에 1개만 나오는게 정상
        print(type(data)) # (  ) 1개가 나오고  튜플로 온다.

        # session => 로그인한 데이터를 세이브해놓는다.
        if data:
            request.session['userid'] = data[0]
            request.session['username'] = data[1]
            return redirect('/member/index')

        return redirect("/member/index")

def logout(request):
    if request.method=="GET" or request.method == 'POST':
        del request.session['userid']
        del request.session['username']
        return redirect('/member/index')

@csrf_exempt
def edit(request):
    if request.method == 'GET':
        ar = [request.session['userid']]
        sql = """
            SELECT * 
            FROM MEMBER 
            WHERE ID=%s
        """
        cursor.execute(sql, ar)
        data = cursor.fetchone()
        return render(request, 'member/edit.html', {"one":data})

    if request.method == 'POST':
        ar = [
            request.POST['name'], 
            request.POST['age'], 
            request.POST['id']
        ]

        sql = """
            UPDATE MEMBER SET NAME=%s, AGE=%s
            WHERE ID=%s
        """
        cursor.execute(sql, ar)
        return redirect("/member/index")

@csrf_exempt
def delete(request):
    if request.method=="GET" or request.method == 'POST':
        ar = [request.session['userid']]
        sql ="""
            DELETE FROM MEMBER WHERE ID=%s
        """
        cursor.execute(sql, ar)
        return redirect("/member/logout")

@csrf_exempt
def join1(request):
    if request.method == 'GET':
        return render(request, 'member/join1.html')
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        pw = request.POST['pw']
        email = request.POST['email']
        tel = request.POST['tel']
        img = request.POST['img']

        ar = [id, name, pw, email, tel, img]

        
        sql = """
        INSERT INTO MEMBER1(ID, NAME, PW, EMAIL, TEL, IMG, JOINDATE) 
        VALUES (%s, %s, %s, %s, %s, %s, SYSDATE)
        """
        cursor.execute(sql,ar)

        print(ar)

        return redirect("/member/index") # 절대경로로 줘라!!, /로 시작해야 한다..

def auth_join(request):
    if request.method == 'GET':
        return render(request, 'member/auth_join.html')
    if request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['first_name']
        em = request.POST['email']
        
        obj = User.objects.create_user(
            username=id, 
            password=pw, 
            first_name=na,
            email=em
        )
        obj.save()
        return redirect("/member/auth_index")

def auth_index(request):
    if request.method == 'GET':
        return render(request, 'member/auth_index.html')
    if request.method == 'POST':
        pass

def auth_login(request):
    if request.method == 'GET':
        return render(request, 'member/auth_login.html')
    if request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']

        # DB에 인증
        obj = auth1(request, username=id, password=pw)

        if obj is not None:
            login1(request, obj) # 세션에 추가

        return redirect("/member/auth_index")

def auth_logout(request):
    if request.method == 'GET' or request.method == 'POST':
        logout1(request)
        return redirect("/member/auth_index")

def auth_edit(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")

        obj = User.objects.get(username=request.user)

        return render(request, "member/auth_edit.html", {"obj": obj})
    if request.method == 'POST':
        id = request.POST['username']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.get(username=id)
        obj.first_name = na
        obj.email = em
        obj.save()
        return redirect("/member/auth_index")

def auth_pw(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")

        return render(request, "member/auth_pw.html")
    if request.method == 'POST':
        pw = request.POST['pw']     # 기존 비밀번호
        pw1 = request.POST['pw1']   # 변경 비밀번호
        # 바꾸기 전에 인증
        obj = auth1(request, username=request.user, password=pw)

        if obj:
            obj.set_password(pw1)
            obj.save()
            return redirect("/member/auth_index")
        return redirect("/member/auth_pw")

def exam_index(request):
    if request.method == 'GET':
        return render(request, "member/exam_index.html")
    if request.method == 'POST':
        pass

def exam_insert(request):
    if request.method == 'GET':
        return render(request, "member/exam_insert.html")
    if request.method == 'POST':
        obj = Table2()
        obj.name = request.POST['name']
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.classroom = request.POST['classroom']
        obj.save()

        return redirect("/member/exam_index")

def exam_insert_many(request):
    if request.method == 'GET':
        return render(request, "member/exam_insert_many.html", {"cnt":range(5)})
    if request.method == 'POST':
        na = request.POST.getlist("name[]")
        ko = request.POST.getlist("kor[]")
        en = request.POST.getlist("eng[]")
        ma = request.POST.getlist("math[]")
        clroom = request.POST.getlist("classroom[]")

        objs = []
        for i in range(0,len(na)):
            obj = Table2()
            obj.name = na[i]
            obj.kor = ko[i]
            obj.eng = en[i]
            obj.math = ma[i]
            obj.classroom = clroom[i]
            objs.append(obj)
        # objs.save()
        Table2.objects.bulk_create(objs)

        return redirect("/member/exam_index")

def exam_select(request):
    if request.method == 'GET':
        # ######  ↓ 안봐도 됨 ↓  ###################################
        #         # SELECT SUM(math) FROM MEMBER_TABLE2
        #         test = Table2.objects.aggregate(Sum("math"))
        #         test = Table2.objects.raw("SELECT SUM(math) FROM MEMBER_TABLE2") 
        #         # 출력은 <RawQuerySet: SELECT SUM(math) FROM MEMBER_TABLE2> 값은 정상적으로 가는 듯

        #         # SELECT NO, NAME FROM MEMBER_TABLE2
        #         test = Table2.objects.all().values('no','name')

        #         # SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC
        #         list = Table2.objects.all().order_by('name')
        #         #list = Table2.objects.raw("SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC")

        #         # 반별 국어, 영어, 수학 합계
        #         # SELECT SUM(kor) AS kor, SUM(eng) AS eng, SUM(math) AS math FROM MEMBER_TABLE2 GROUP BY CLASSROOM
        #         test = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))
        # ######  ↑ 안봐도 됨 ↑  ###################################

        # classroom 전체 가져오기
        rows_tmp = Table2.objects.all().values("classroom")
        tmp = set()
        for i in rows_tmp:
            tmp.add(i['classroom'])
        clsroom = list(tmp)
        clsroom.sort()

        # 페이지 넘버링
        page = int(request.GET.get("page", 1))
        
        # 1 - 0~9
        # 2-  10~19
        page_end = page*10
        page_start = page_end-10

        cnt = Table2.objects.all().count()
        tot = (cnt-1)//10 + 1

        # 검색
        txt = request.GET.get("txt", "")
        
        cls = request.GET.get("cls", 0)
        if cls:
            # rows = Table2.objects.filter(classroom=cls)
            if not txt:
                sql = "SELECT * FROM MEMBER_TABLE2 WHERE CLASSROOM="+cls
                rows = Table2.objects.raw(sql)[page_start:page_end]
                sum_avg_list = sum_avg(sql)

                return render(request, "member/exam_select.html", 
                    {"list":rows, "classroom_list":clsroom, "sum_avg":sum_avg_list, "pages":range(1,tot+1), "cls":cls})
            else: # txt exist
                sql = "SELECT * FROM MEMBER_TABLE2 WHERE CLASSROOM=" + cls + "and  NAME LIKE '%%" + txt + "%%'" 
                rows = Table2.objects.raw(sql)[page_start:page_end]
                sum_avg_list = sum_avg(sql)

                return render(request, "member/exam_select.html", 
                    {"list":rows, "classroom_list":clsroom, "sum_avg":sum_avg_list, "pages":range(1,tot+1), "cls":cls,"txt":txt})
        else:
            if not txt:
                sql = "SELECT * FROM MEMBER_TABLE2 ORDER BY classroom"
                rows = Table2.objects.raw(sql)[page_start:page_end]
                sum_avg_list = sum_avg(sql)

                return render(request, "member/exam_select.html", 
                    {"list":rows, "classroom_list":clsroom, "sum_avg":sum_avg_list, "pages":range(1,tot+1)})
            else: # txt exist
                # rows = Table2.objects.all().order_by('classroom')
                # cnt = Table2.objects.filter(name__contains==txt).count()
                # tot = (cnt-1)//10-1

                sql = "SELECT * FROM MEMBER_TABLE2 WHERE NAME LIKE '%%" + txt + "%%'" + " ORDER BY classroom "
                rows = Table2.objects.raw(sql)[page_start:page_end]
                sum_avg_list = sum_avg(sql)

                return render(request, "member/exam_select.html", 
                    {"list":rows, "classroom_list":clsroom, "sum_avg":sum_avg_list, "pages":range(1,tot+1),"txt":txt})

def sum_avg(sql):
    # sum_list = Table2.objects.raw("SELECT 1 as no, SUM(kor) as skor, SUM(eng) as seng, SUM(math) as smath FROM MEMBER_TABLE2")
    sqlS = "SELECT 1 as no, SUM(kor) as skor, SUM(eng) as seng, SUM(math) as smath FROM ("+ sql + ")"
    sqlA = "SELECT 1 as no, AVG(kor) as akor, AVG(eng) as aeng, AVG(math) as amath FROM ("+ sql + ")"
    sum_list = Table2.objects.raw(sqlS)
    avg_list = Table2.objects.raw(sqlA)
    sum_avg_list = [
        sum_list[0].skor,
        sum_list[0].seng,
        sum_list[0].smath,
        # avg_list[0].akor,
        int(avg_list[0].akor),
        # avg_list[0].aeng,
        int(avg_list[0].aeng),
        # avg_list[0].amath,
        int(avg_list[0].amath),
    ]
    return sum_avg_list

def exam_update(request):
    if request.method == 'GET':
        n = request.GET.get("no", 0)
        row = Table2.objects.get(no=n)
        clsroom = Table2.objects.get
        return render(request, "member/exam_update.html",{"one": row})
    if request.method == 'POST':
        n = request.POST["no"]
        obj = Table2.objects.get(no=n)

        obj.name = request.POST["name"]
        obj.kor = request.POST["kor"]
        obj.eng = request.POST["eng"]
        obj.math = request.POST["math"]
        obj.classroom = request.POST["classroom"]
        obj.save()

        return redirect("/member/exam_select")

def exam_delete(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)

        row = Table2.objects.get(no=n)
        row.delete()
        return redirect("/member/exam_select")
    if request.method == 'POST':
        pass

def js_index(request):
    if request.method == 'GET':
        return render(request, "member/js_index.html")
    if request.method == 'POST':
        pass

def js_chart(request):
    if request.method == 'GET':
        return render(request, "member/js_chart.html")
    if request.method == 'POST':
        pass

def dataframe(request):
    if request.method == 'GET':
        # 1. QuerySet >> list 변경
        # SELECT NO, NAME, KOR FORM MEMBER_TABLE2
        rows = list(Table2.objects.all().values("no","name", "kor"))
        print(rows) # >> [{ }, { }, ...  ] dict의 list

        # 2. list >> dataframe 변경
        df = pd.DataFrame(rows)

        # 3. dataframe >> list 변경
        rows1 = df.values.tolist()
        print(rows) # >> [( ), ( ), ...  ]list의 list
        
        return render(request, "member/dataframe.html", {"df_table": df.to_html, "list":rows})
    if request.method == 'POST':
        pass

def graph(request):
    if request.method == 'GET':
        
        # 폰트 읽기
        font_name = font_manager.FontProperties\
            (fname="c:/Windows/Fonts/malgun.ttf").get_name()
        # 폰트 적용
        rc('font', family=font_name)

        sum_list = Table2.objects.values("classroom").annotate(skor=Sum("kor"), seng=Sum("eng"), smath=Sum("math"))
        print(sum_list)
        
        # classroom 전체 가져오기
        rows_tmp = Table2.objects.all().values("classroom")
        tmp = set()
        for i in rows_tmp:
            tmp.add(i['classroom'])
        clsroom_list = list(tmp)
        clsroom_list.sort()

        # 이미지 데이터 리스트
        img_list = []

        # 전체에서 합계
        skor = Table2.objects.aggregate(skor = Sum("kor"))['skor']
        seng = Table2.objects.aggregate(seng = Sum("eng"))['seng']
        smath = Table2.objects.aggregate(smath = Sum("math"))['smath']
        x = ['all_kor', 'all_eng', 'all_math']
        y = [skor, seng, smath]

        plt.bar(x,y)
        plt.title("All_SUM")
        plt.xlabel("과목")
        plt.ylabel("성적")

        # plt.show() # 표시, web에서는 출력 안됨
        plt.draw() # 안보이게 그림을 캡처 
        img = io.BytesIO() # img에 byte배열로 보관
        plt.savefig(img, format="png") # png파일 포맷으로 저장
        img_url = base64.b64encode(img.getvalue()).decode()
        img_list.append(img_url)

        plt.close() # 그래프 종료
        
        # 반 별로 for 돌면서 그래프
        for i in clsroom_list:
            clsroom = str(i)
            # skor = Table2.objects.filter(classroom=101).aggregate(skor = Sum("kor"))['skor']
            # SELECT 1 as no, SUM('kor) as skor FROM MEMBER_TABLE2
            
            skor = Table2.objects.filter(classroom=clsroom).aggregate(skor = Sum("kor"))['skor']
            seng = Table2.objects.filter(classroom=clsroom).aggregate(seng = Sum("eng"))['seng']
            smath = Table2.objects.filter(classroom=clsroom).aggregate(smath = Sum("math"))['smath']
            x = [clsroom+'_kor', clsroom+'_eng', clsroom+'_math']
            y = [skor, seng, smath]

            plt.bar(x,y)
            plt.title(clsroom+"_SUM")
            plt.xlabel("과목")
            plt.ylabel("성적")

            # plt.show() # 표시, web에서는 출력 안됨
            plt.draw() # 안보이게 그림을 캡처 
            img = io.BytesIO() # img에 byte배열로 보관
            plt.savefig(img, format="png") # png파일 포맷으로 저장
            img_url = base64.b64encode(img.getvalue()).decode()
            img_list.append(img_url)
            plt.close() # 그래프 종료

        new_list = []
        for i in img_list:
            new_list.append( "data:;base64,{}".format(i) )

        return render(request, "member/graph.html", {"graphs": new_list, "len": range(len(new_list))})
        # <img src="{{graph}}" />

######  SQL 추가 설명  ####################################
        # SELECT SUM("kor") FROM MEMBER_TABLE2 WHERE KOR > 10
        # > gt, >= gte, < lt, <= lte
        skor = Table2. objects.filter(kor__gt=10).aggregate(skor=Sum("kor"))[skor]

        # SELECT SUM("kor") skor, SUM("eng") seng, SUM("math") smath
        # FROM MEMBER_TABLE2 GROUP BY CLASSROOM
        sum_list = Table2.objects.values("classroom").annotate(skor=Sum("kor"), seng=Sum("eng"), smath=Sum("math"))





######  SQL 추가 설명  ####################################
    if request.method == 'POST':
        pass
