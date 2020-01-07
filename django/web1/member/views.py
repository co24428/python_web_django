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

              
# Create your views here.
def index(request):
    # return HttpResponse("indexpagesssss")
    return render(request, 'member/index.html')

def list(request):
    # ID 기준으로 오름차순
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql)
    data = cursor.fetchall();
    print(type(data))
    print(data)
    
    # list.html을 표시하기 전에
    # list 변수에 data값을, title변수에 "회원목록" 문자를
    # template에서는 최대한 상수 쓰지말라. view단에서 넘기는 것이 최선의 방법 !!
    return render(request, 'member/list.html', {"list":data, "title": "회원목록"})

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