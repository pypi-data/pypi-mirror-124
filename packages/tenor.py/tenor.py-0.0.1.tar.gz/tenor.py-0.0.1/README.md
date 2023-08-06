# **TENOR**

파이썬용 Gif 라이브러리입니다.

- https://pypi.org/projects/tenor
- https://github.com/cord0318/python_tenor

# **Download**

```shell
pip install tenor
```

# **How To Use**

```python
# 비동기
import tenor
import asyncio

async def main():
    print(await tenor.asyncSearchGif("gif 이름", "가져올 수", "다운로드 확인", "다운로드 경로"))

asyncio.get_event_loop().run_until_complete(main())
```

```python
# 동기
import tenor

print(tenor.searchGif("gif 이름", "가져올 수", "다운로드 확인", "다운로드 경로"))
```

# **Tip**

*이 모듈을 사용하여 디스코드 봇을 만들수 있습니다!*