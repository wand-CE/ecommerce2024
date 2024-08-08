from django.urls import path
from pedidos import views

urlpatterns = [
    path('add/', views.PedidoCreateView.as_view(), name='addpedido'),
    path('resumo/', views.ResumoPedidoTemplateView.as_view(),
         name='resumopedido'),
]