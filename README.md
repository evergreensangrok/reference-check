## Reference Check
* 사용자간 평판을 요청하고 조회할 수 있는 API 

## Feature
* JWT를 이용한 인증/인가
* 지원자가 평가자에게 평판작성을 요청하는 기능
* 작성자가 요청받은 평판에 대한 작성 기능
* 기업 관리자가 평판을 조회하는 기능

## Code 구조

```
├── project
│   ├── settings.py           (프로젝트 설정)
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── reference                 (Reference app)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             (평판관련 모델)
│   ├── permissions.py        (권한설정 코드)
│   ├── serializers.py        (serializer)
│   ├── tests.py              (테스트 코드)
│   ├── urls.py
│   └── views.py              (View functions)
├── requirements.txt
├── setup.cfg
├── user                      (User app)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             (유저관련 모델)
│   ├── serializers.py        (serializer)
│   ├── tests.py              (테스트 코드)
│   ├── urls.py
│   └── views.py
├── manage.py
├── .github\workflow
│   └── ci.yaml               (github action CI)
├── .pre-commit-config.yaml   (pre-commit hook)
├── .isort.cfg                (isort)
├── setup.cfg                 (flake8)
├── setup.cfg
└── pytest.ini                (pytest configuration)
```
