from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import SighupForm,SighnInForm,ExpenseForm

from django.contrib.auth import authenticate,login,logout

from myapp.models import Expense

from django.db.models import Sum,Count

from myapp.decorators import signin_requred

from django.utils.decorators import method_decorator    #to convert function deco => method deco

from django.contrib import messages



# Create your views here.

class SighnupView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SighupForm()
        
        return render(request,"register.html",{"form":form_instance})



    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=SighupForm(form_data)

        if form_instance.is_valid():

            form_instance.save()

            print (">>>>>>>ACCOUNT CREATED<<<<<<<<<")

            messages.success(request,"Successfully Account Created")

            return redirect("sighnin")
        
        else:

            print(">>>>>>ACCOUNT CREATION FAILED<<<<<<<<")

            messages.error(request,"Account Creation Failed")

            return render(request,"register.html",{"form":form_instance})

            
class SighInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SighnInForm()

        # messages.success(request,"please sighnup")

        return render(request,"sighnin.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=SighnInForm(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_instance=authenticate(request,username=uname,password=pwd)

            if user_instance:

                login(request,user_instance)

                print(">>>>>>success<<<<<")

                messages.success(request,"signed successfully")

                return redirect("index")
            
            else:
                print(">>>>>failed<<<<<")

                messages.error(request,"some error have been there please check")

                return render(request,"sighnin.html",{"form":form_instance})

@method_decorator(signin_requred,name="dispatch")   

class IndexView(View):

    def get(self,request,*args,**kwargs):

        total_expense=Expense.objects.filter(owner=request.user).values("amount").aggregate(total=Sum("amount"))

        print(total_expense)

        category_summary=Expense.objects.filter(owner=request.user).values("category").annotate(total=Sum("amount"),count=Count("category")).order_by("-total")

        print(category_summary)

        context={
            "total_expense":total_expense.get("total"),

            "category_summary":category_summary
        }

        return render(request,"index.html",context)
    
        
@method_decorator(signin_requred,name="dispatch") 

class sighnoutView(View):

          


    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("sighnin")

@method_decorator(signin_requred,name="dispatch")         

class ExpenseCreateView(View):

           


    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()


        qs=Expense.objects.filter(owner=request.user).order_by("-created_at")

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=ExpenseForm(form_data)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            messages.success(request,"expense successfully added")

            return redirect("expense-add")
        
        else:

            return render(request,"sighnin.html",{"form":form_instance})
@method_decorator(signin_requred,name="dispatch")  

class  ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"Expense Deleted")

        return redirect("expense-add")
    
@method_decorator(signin_requred,name="dispatch")   
class ExpenseUpdateVIew(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_object)

        return render(request,"expense_update.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_data=request.POST

        form_instance=ExpenseForm(form_data,instance=expense_object)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"Expense Updated")

            return redirect("expense-add")
        
        else:

            return render(request,"expense_update.html",{"form":form_instance})



    

        





    