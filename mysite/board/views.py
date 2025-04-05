import os
import uuid
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from mysite import settings

from .models import Board
from .forms import BoardForm, BoardDeleteForm

# 등록
def board_create(request):
    # 입력 폼 (비어있는 값)
    form = BoardForm()
    
    # 처리
    if request.method == "POST":
      
        # 입력 폼 (사용자로부터 받은 값)
        form = BoardForm(request.POST) # request : 사용자로 부터 넘어온 정보 # 얘네를 form으로 넘겨준다.
       
        # 입력 폼 유효성 검사
        # 검사 통과
        if form.is_valid(): #is_valid : 검증하는 단계
            board = form.save(commit=False) # 저장
            
            # 파일 업로드
            if request.FILES:
                filename = uuid.uuid4().hex
                file = request.FILES.get("file")
                
                # 파일 저장
                save_path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(save_path, 'wb') as f:
                    for chunk in file.chunks(): # chunk단위로 쪼개서 실행
                        f.write(chunk)
                        
                # 파일이 있을 때만 추가가 되기 때문에 파일이 없으면 밑에 2줄은 blank로 들어간다.
                # models.py에서 blank=True로 해놨기 때문
                board.filename = filename
                board.original_filename = file.name
                
            board.save()
            
            messages.success(request, "게시글이 등록되었습니다.")
            return redirect("board:read", board_id=board.id)
        
        # 검사 실패
        else:
            for field_name, error_messages in form.errors.items():
                messages.error(request, f"{form.fields[field_name].label} : {error_messages[0]}")
    
    # GET 요청일 때 폼 반환
    form = BoardForm()
           
    # 화면
    return render(request, "board/create.html", {"form": form})

    
# 상세보기
def board_read(request, board_id):
    board = Board.objects.get(id=board_id)
    context = {"board": board}
    return render(request, "board/read.html", context)


# 수정
def board_update(request, board_id):
    board = Board.objects.get(id=board_id)
    context = {"board": board}
    old_password = board.password

    # POST 요청일 때
    if request.method == "POST":
        # 입력 폼(사용자로부터 받은 값)
        form = BoardForm(request.POST, instance=board)

        # 입력 폼 유효성 검사
        # 검사 통과
        if form.is_valid():
            new_password = form.cleaned_data.get("password")

            if old_password == new_password:
                # 게시글 수정
                board = form.save(commit=False)  # 들어온 정보를 저장
                
                if request.FILES:
                    # 파일 삭제가 체크되어 있거나 기존 파일이 있으면 기존 파일 삭제
                    if request.POST.get("deleteFile") or board.filename:
                        os.remove(os.path.join(settings.MEDIA_ROOT, board.filename))
                    
                    filename = uuid.uuid4().hex
                    file = request.FILES.get("file")
                    
                    # 파일 저장
                    save_path = os.path.join(settings.MEDIA_ROOT, filename)
                    with open(save_path, 'wb') as f:
                        for chunk in file.chunks():
                            f.write(chunk)
                    
                    board.filename = filename
                    board.original_filename = file.name
                
                board.save()

                messages.success(request, "게시글이 수정되었습니다.")
                return redirect("board:read", board_id=board.id)

            else:
                messages.error(request, "비밀번호가 일치하지 않습니다")

        # 검사 실패
        else:
            for field_name, error_messages in form.errors.items():
                messages.error(
                    request, f"{form.fields[field_name].label}: {error_messages[0]}"
                )
    # GET 요청일 때 빈 폼 반환
    form = BoardForm(instance=board)
    context["form"] = form

    # 화면
    return render(request, "board/update.html", context)


# 삭제
def board_delete(request, board_id):
    board = Board.objects.get(id=board_id)
    old_password = board.password

    if request.method == "POST":
        form = BoardDeleteForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("password")
            
            if old_password == new_password:
                # 파일 삭제
                # os.remove(os.path.join(settings.MEDIA_ROOT, board.filename))
                
                # 파일이 존재할 때만 삭제 시도
                file_path = board.filename
                if file_path:  
                    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        
                board.delete()
                return HttpResponse("게시글이 삭제되었습니다.")
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
                return redirect("board:read", board_id=board.id)

# 목록
def board_list(request):
    # 테스트 글 추가
    # 예시 글 300개 추가한거라서 300개 필요없으면 주석처리 하면됨(밑에 2줄) 한번만 하면 됨 이미 했다. 지금은 필요없당
    #for i in range(1,300):
       # Board.objects.create(title=f"제목 {i}", content=f"내용  {i}", password="1234", created_by="홍길동")
    page = request.GET.get('page', '1') #page가 없으면 기본 1로 가져온다.
    keyword = request.GET.get('keyword','') #keyword가 없으면 ''을 가져온다.
    search_type = request.GET.get('search_type','')
    boards = Board.objects.all().order_by('-created_at')

    if keyword:
        if search_type == 'title':
            boards = boards.filter(Q(title__icontains=keyword))
        elif search_type == 'content':
            boards = boards.filter(Q(content__icontains=keyword))
        elif search_type == 'created_by':
            boards = boards.filter(Q(created_by__icontains=keyword))
        elif search_type == 'all':
            boards = boards.filter(
                Q(title__icontains=keyword) |
                Q(content__icontains=keyword) |
                Q(created_by__icontains=keyword)
            )
        # Q:장고에서 필터처리를 하기위해 제공해주는 라이브러리
        # 키워드가 있다면 필터를 이용해서 값을 가져온다.
    
    paginator = Paginator(boards, 10)
    page_obj = paginator.get_page(page)

    context = {
        "boards" : page_obj,
        "keyword" : keyword,
        "search_type" : search_type,
    }
    
    return render(request, "board/list.html", context)

# 파일 다운로드
def board_download(request, board_id):
    board = Board.objects.get(id=board_id)
    file_path = os.path.join(settings.MEDIA_ROOT, board.filename)
    return FileResponse(
        open(file_path, 'rb'),
        as_attachment = True,
        filename = board.original_filename
    )