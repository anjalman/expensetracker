from django.shortcuts import render,get_object_or_404

from rest_framework.response import Response

from rest_framework.views import APIView

from myapp.models import Expense

from api.seriailizers import UserCreationSerializer,ExpenseSerializer

from rest_framework import authentication,permissions

from rest_framework import serializers


# Create your views here.

class UserCreateView(APIView):

    def post(self,request,*args,**kwargs):

        serialaizer_instance=UserCreationSerializer(data=request.data)

        if serialaizer_instance.is_valid():

            serialaizer_instance.save()

            return Response(data=serialaizer_instance.data)
        
        else:

            return Response(data=serialaizer_instance.errors)
        
class ExpenseListCreateView(APIView):

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=Expense.objects.filter(owner=request.user)

        serializer_instance=ExpenseSerializer(qs,many=True)

        return Response(data=serializer_instance.data)


    def post(self,request,*args,**kwargs):

        serialiser_instance=ExpenseSerializer(data=request.data) #deserialization

        if serialiser_instance.is_valid():

            serialiser_instance.save(owner=request.user)

            return Response(data=serialiser_instance.data)
        
        else:

            return Response(data=serialiser_instance.errors)

class ExpenseRetriveUpdateDestroyView(APIView):

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_instance=get_object_or_404(Expense,id=id)

        if expense_instance.owner != request.user:

            raise serializers.ValidationError("you have no access")

        serializer_instance=ExpenseSerializer(expense_instance)

        return Response(data=serializer_instance.data)
    
    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_instance=get_object_or_404(Expense,id=id)

        serializer_instance=ExpenseSerializer(data=request.data,instance=expense_instance)

        if serializer_instance.is_valid():

            serializer_instance.save()
            
            return Response(data=serializer_instance.data)
        else:

            return Response(data=serializer_instance.errors)
        
    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_instance=get_object_or_404(Expense,id=id)

        if expense_instance.owner != request.user:

            raise serializers.ValidationError("you have no access")
        
        expense_instance.delete()

        return Response(data={"message":"delete"})









