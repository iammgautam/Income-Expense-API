from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:id>/', views.RetrieveUpdateDestroyAPIView.as_view(), name='expenses-id'),
]
