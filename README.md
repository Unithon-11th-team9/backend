# backend

<br><br>

## 가상 환경

pyenv 를 설치합니다.

```
curl https://pyenv.run | bash
```

python 을 설치합니다.

```
pyenv install 3.11.4
```

가상환경을 생성합니다.

```
pyenv virtualenv 3.11.4 가상환경이름
```

가상환경에 진입합니다.

```
pyenv activate 가상환경이름
```

<br><br>

## 종속성 관리

poetry 를 설치합니다.

```
curl -sSL https://install.python-poetry.org | python3 -
```

의존성 패키지를 설치합니다.

```
poetry install
```

의존성 패키지 추가 명령어

```
poetry add 패키지이름
```

의존성 패키지 제거 명령어

```
poetry remove 패키지이름
```

<br><br>

## pre-commit

pre-commit hook 설치

```
pre-commit install
```

<br><br>

## 서버 실행

스크립트 권한을 추가합니다.

```
chmod +x scripts/* 
```

서버 실행 명령어

```
scripts/run-server.sh
```

개발 서버 실행 명령어(변경사항 실시간 반영)

```
scripts/dev.sh
```

<br><br>

## API 명세

OpenAPI

```
http://0.0.0.0:8000/docs
```

```
http://0.0.0.0:8000/redoc
```
