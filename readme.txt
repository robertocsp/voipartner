Para instalar a aplicação localmente:

1) Criar uma virtualenv com Python3
2) Ativar a venv (source bin/activate)
3) Instalar os requerimentos da virtualenv (pip freeze -r requirements.txt)
4) Criar variável de ambiente: export DJANGO_SETTINGS_MODULE=voipartnerproject.local
5) Rodar o python manage.py makemigrations
6) Rodar o python manage.py migrate
7) Criar o super usuário - python manage.py createsuperuser

======
Se pycharm
1) Criar o interpretador da virtualenv
    Pycharm > Preferences > Project > Project Interpreter
    Nova variável
    De ambiente existente
    Apontar para o bin/python3
2) Para rodar o projeto criar variável de ambiente no pycharm. Para isso:
    Editar as configurações de execução
    Adicionar a variável em Environment Variables.


========

Credenciais SMTP SES
SMTP Username: AKIAJXOGL3CGO4CXDGRQ
SMTP Password: AlrvPsS02s0sUEsBtjuWDVLVmAVeC7EEpbLzm9zGpWfq

