# team9-api

## Requirements
* Python 3.11.4
* Poetry **
* Docker & Docker Compose
* (Optional) Postgresql **

## Conventions
### Branches
* `main (default)`: (~~) 으로 배포
* `feature/{description}`: 새로운 기능이 추가되는 경우에 사용
* `refactor/{description}`: 기능 변경 없이 코드 리팩토링만을 하는 경우에 사용
* `fix/{description}`: `main` 브랜치로 반영하는 사소한 오류 수정 시에 사용

### PR Merge Rules
* default: *Squash and merge*
<br><br>
# Dev Guidelines

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

## Server Startup
Docker Compose를 활용하여 FastAPI 서버를 실행합니다
```
docker-compose up
```


쉘 스크립트로 실행하려면 아래와 같이

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

## Deployment
main 브랜치에 새로운 push가 일어날 때마다, Github Actions를 통해 자동으로 배포가 이루어집니다.

## API 명세

OpenAPI

```
http://0.0.0.0:8000/docs
```

```
http://0.0.0.0:8000/redoc
```

<br><br>

## Migration
alembic 과 manage.py 를 이용하여 migration 합니다.

makemigrations(versions) 파일 생성 명령어
```py
python manage.py makemigrations
```

migrate(upgrade) 실행 명령어
```py
python manage.py migrate
```

downgrade 실행 명령어
```py
python manage.py downgrade
```

