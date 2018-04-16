"""voipartnerproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from voipartner import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<str:filename>', views.download, name='download'),
    path('', views.home, name='home'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.my_login, name='my_login'),
    path('logout', views.my_logout, name='my_logout'),
    path('contratos', views.contratos_usuario, name='contratos_usuario'),
    path('contratos-pendentes', views.contratos_pendentes, name='contratos_pendentes'),
    path('contratos-em-vigor', views.contratos_em_vigor, name='contratos_em_vigor'),
    path('contratos-encerrados', views.contratos_encerrados, name='contratos_encerrados'),
    path('contratos/<int:contrato_id>', views.contrato, name='contrato'),
    path('contratos/<int:contrato_id>/pagamento-pendente', views.contrato_pendente_pagamento, name='contrato-pendente-pagamento'),

]

#Para produção podemos servir com o NGINX, porem o ideal é fazer algum acesso privado com controle de acesso
'''
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''