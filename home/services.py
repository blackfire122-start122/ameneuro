from pathlib import Path
from typing import IO, Generator
from django.shortcuts import get_object_or_404
from .models import Post, Music

import random
import string


strings = string.ascii_letters+string.digits

def gen_rand_id(n):
	res = ""
	for i in range(n):res+=random.choice(strings)
	return res

def del_friends(user_friends,user):
	for f in range(len(user_friends)):
		for fc in user_friends[f].chats.all():
			for uc in user.chats.all():
				if uc == fc:
					del user_friends[f]
					return del_friends(user_friends,user)
	return user_friends

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