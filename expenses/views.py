from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from expenses.serializers import ExpensesSerializers
from expenses.models import Expense
from expenses.permissions import IsOwner
# Create your views here.

class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpensesSerializers
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,) #this is work only if user is authenticated.

    #this fuction returns the expense list of that particular logged in user.
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    #this function with return the queryset of the loggedIn user's expense list 
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializers
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner) #this is work only if user is authenticated.
    lookup_fields = 'id' #this will loopkup of a specific expense details of the authenticate user.

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)