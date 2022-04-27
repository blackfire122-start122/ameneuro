from pathlib import Path
from typing import IO, Generator
from django.shortcuts import get_object_or_404
from .models import Post, Music, Chat, Message, User, Video
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden

import random
import string
from ameneuro.settings import get_videos_how, get_posts_how, get_elements_how, get_user_how

strings = string.ascii_letters+string.digits

def gen_rand_id(n):
    res = ""
    unicue = True
    for i in range(n):res+=random.choice(strings)

    while unicue:
        if Chat.objects.filter(chat_id=res):
            for i in range(n):res+=random.choice(strings)
        else:unicue = False
    return res

def ranged(file: IO[bytes],start: int = 0,end: int = None,block_size: int = 8192,) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, id, type_s) -> tuple:
    if type_s == 'post':
        _file = get_object_or_404(Post, pk=id)
    elif type_s == 'music':
        _file = get_object_or_404(Music, pk=id)
        request.session['music_id'] = id
    elif type_s == 'mess':
        _file = get_object_or_404(Message, pk=id)
        request.session['music_id'] = id
    elif type_s == 'video':
        _file = get_object_or_404(Video, pk=id)

    path = Path(_file.file.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, content_range

def get_posts(data,user):
    posts = {}
    if not defence_isdigit(data.get("start_element"),
        data.get("end_element"),
        data.get("start_rec_post"),
        data.get("end_rec_post"),
        data.get("start_rec_user"),
        data.get("end_rec_user"),
        data.get("defolt_posts")
    ):return [None,None,HttpResponseBadRequest]

    start = int(data.get("start_element"))
    end = int(data.get("end_element"))

    try:
        friends = user.friends.all()
        follow = user.follow.all()
        posts = Post.objects.filter(user_pub__in=friends|follow).order_by("-date")[start:end]
        if len(posts)<get_posts_how:
            start_rec_post = int(data.get("start_rec_post"))
            end_rec_post = int(data.get("end_rec_post"))

            start_rec_user = int(data.get("start_rec_user"))
            end_rec_user = int(data.get("end_rec_user"))

            rec_user = User.objects.exclude(pk__in=friends|follow)[start_rec_user:end_rec_user]
            posts |= Post.objects.filter(user_pub__in=rec_user).order_by("-date")[start_rec_post:end_rec_post]
            
            if int(data.get("defolt_posts"))==1: 
                start_rec_post = 0
                end_rec_post = get_posts_how
                data["defolt_posts"]=0
            
            if int(data.get("start_rec_user")) > User.objects.count():
                return [posts,data,None]
            if len(posts)<get_posts_how:
                data["defolt_posts"]=1

                start_rec_user+=get_user_how
                end_rec_user+=get_user_how

                data["start_rec_user"]=start_rec_user
                data["end_rec_user"]=end_rec_user

                posts |= get_posts(data,user)[0]

            start_rec_post+=get_posts_how
            end_rec_post+=get_posts_how

            data["start_rec_post"]=start_rec_post
            data["end_rec_post"]=end_rec_post

    except:return [None,None,None]

    start+=get_posts_how
    end+=get_posts_how

    data["start_element"]=start
    data["end_element"]=end
    return [posts,data,None]

def get_videos(request):
    videos = {}
    start = request.session["start_element_video"]
    end = request.session["end_element_video"]

    try:
        friends = request.user.friends.all()
        follow = request.user.follow.all()
        videos = Video.objects.filter(user_pub__in=friends|follow).order_by("-date")[start:end]
        if len(videos)<get_videos_how:
            start_rec_video = request.session["start_rec_video"]
            end_rec_video = request.session["end_rec_video"]

            start_rec_video_user = request.session["start_rec_video_user"]
            end_rec_video_user = request.session["end_rec_video_user"]

            rec_user = User.objects.exclude(pk__in=friends|follow)[start_rec_video_user:end_rec_video_user]
            videos |= Video.objects.filter(user_pub__in=rec_user).order_by("-date")[start_rec_video:end_rec_video]
        
            if request.session["defolt_video"]: 
                start_rec_video = 0
                end_rec_video = get_videos_how
                request.session["defolt_video"] = False
            
            if request.session["start_rec_video_user"] > User.objects.count():
                return videos
            if len(videos)<get_videos_how:
                request.session["defolt_video"] = True

                start_rec_video_user+=get_user_how
                end_rec_video_user+=get_user_how

                request.session["start_rec_video_user"]=start_rec_video_user
                request.session["end_rec_video_user"]=end_rec_video_user

                videos |= get_videos(request)

            start_rec_video+=get_videos_how
            end_rec_video+=get_videos_how

            request.session["start_rec_video"]=start_rec_video
            request.session["end_rec_video"]=end_rec_video

    except:return {}

    start+=get_videos_how
    end+=get_videos_how

    request.session["start_element_video"]=start
    request.session["end_element_video"]=end
    return videos

def defence_isdigit(*args):
    return all([str(i).isdigit() for i in args])

def defence_ptl(a,b):
    return int(a)-int(b)==-get_elements_how