
from django.shortcuts import render,redirect
from django.urls import reverse
from urllib.parse import urlencode
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache

# Create your views here.



def index(req):
    return render(req,'home.html',)


@never_cache
def Registration(req):
    if req.method == 'POST':
        n=req.POST.get('name')
        e=req.POST.get('email')
        c=req.POST.get('contact')
        p=req.POST.get('password')
        cp=req.POST.get('cpassword')
        ph=req.FILES.get('photo')
        user = User.objects.filter(Email=e)
        print(user)
        if not user:
            if p == cp:
                User.objects.create(
                    Name=n,
                    Email=e,
                    Contact=c,
                    Pass=p,
                    CPass=cp,
                    Image=ph
                )
                messages.success(req, 'Registration successful. Please login.')
                return redirect('login')
            else:
                msg = "Password and confirm not matched"
                userdata = {'name':n,'contact':c,'email':e}
                return render(req,'Registration.html',{'pmsg':msg,'data':userdata})
        
        else:
            msg='This email already exist'
            return render(req,'Registration.html',{'msg':msg})
    
    return render(req,'Registration.html')


@never_cache
def login(req):
    next_url = req.POST.get('next') or req.GET.get('next', '')
    if req.method=='POST':
        e=req.POST.get('email')
        p=req.POST.get('password')

        if e == 'rahulkahar88588@gmail.com' and p == 'rahul88588':
            a_data = {
                'id': 1,
                'name': 'Rahul',
                'email': 'rahulkahar88588@gmail.com',
                'password': 'rahul88588',
                'image': 'images/admin.png'
            }
            req.session['a_data'] = a_data
            req.session['role'] = 'admin'
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={req.get_host()}):
                return redirect(next_url)
            return redirect('admindashboard')

        user = User.objects.filter(Email=e.strip()).first()
        if user and p.strip() == user.Pass.strip():
            req.session['user_id'] = user.id
            req.session['role'] = 'user'
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={req.get_host()}):
                return redirect(next_url)
            return redirect('userdashboard')

        employee = Add_Employee.objects.filter(Email=e).first()
        if employee and p == employee.Code:
            req.session['emp_id'] = employee.id
            req.session['role'] = 'employee'
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={req.get_host()}):
                return redirect(next_url)
            return redirect('empdashboard')

        messages.warning(req, 'Email or password is incorrect')
        return render(req,'login.html', {'next': next_url})

    return render(req,'login.html', {'next': next_url})


@never_cache
def home(req):
    all_items = Item.objects.all()
    return render(req,'home.html',{'items': all_items,})



@never_cache
def admindashboard(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        return render(req,'admindashboard.html',{'data':a_data})
    else:
        return redirect('login')
    
def market(req):
    return render(req,'market.html')
    


@never_cache
def logout(req):
    req.session.flush()
    return redirect('login')


@never_cache
def add_dep(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
    else:
        return redirect('login')
    
@never_cache
def save_dep(req):
    if 'a_data' in req.session:
        if req.method == 'POST':
           
            dn=req.POST.get('dep_name')
            dd=req.POST.get('dep_desc')
            dh=req.POST.get('dep_head')
            dept=Department.objects.filter(dep_name=dn)
            if dept:
               messages.warning(req,'department already exist')
               a_data= req.session.get('a_data')
               return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
            else:
                Department.objects.create(dep_name=dn,dep_desc=dd,dep_head=dh)
                messages.success(req,'Department created')
                a_data= req.session.get('a_data')
                return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
    else:
        return redirect('login')
    
@never_cache
def show_dep(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        departments = Department.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'show_dep':True, 'departments':departments})
    else:
        return redirect('login')
    

@never_cache
def edit_dep(req, id):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        department = Department.objects.get(id=id)
        return render(req,'admindashboard.html',{'data':a_data, 'edit_dep':True, 'department':department})
    else:
        return redirect('login')


@never_cache
def update_dep(req, id):
    if 'a_data' in req.session:
        if req.method == 'POST':
            department = Department.objects.get(id=id)
            department.dep_name = req.POST.get('dep_name')
            department.dep_desc = req.POST.get('dep_desc')
            department.dep_head = req.POST.get('dep_head')
            department.save()
            messages.success(req, 'Department updated successfully')
        return redirect('show_dep')
    else:
        return redirect('login')


@never_cache
def delete_dep(req, id):
    if 'a_data' in req.session:
        department = Department.objects.filter(id=id).first()
        if department:
            department.delete()
            messages.success(req, 'Department deleted successfully')
        else:
            messages.warning(req, 'Department not found')
        return redirect('show_dep')
    else:
        return redirect('login')


@never_cache
def add_emp(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        departments = Department.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'add_emp':True,'departments':departments})
    else:
        return redirect('login')
    

@never_cache
def save_emp(req):
    if 'a_data' in req.session:
        if req.method == 'POST':
           
            en=req.POST.get('name')
            ee=req.POST.get('email')    
            ec=req.POST.get('contact')
            ed=req.POST.get('dept')
            ei=req.FILES.get('image')
            eco=req.POST.get('code')
            send_mail(
                 "Mail From HR Department",
                 f'this is information regarding your company exdential : \n \n Name={en}, \n Email={ee}, \n Contact={ec}, \n Department={ed} ,\n Code={eco} , \nImage={ei}  \n \n You can login with this Email and Code \n \n Thank you for joining our company and welcome to our team.',
                 "rahulkahar88588@gmail.com",
                 [ee],
                 fail_silently=False,
            )

            emp=Add_Employee.objects.filter(Email=ee)
            if emp:
                messages.warning(req,'Employee already exist')
                a_data = req.session.get('a_data')
                departments = Add_Employee.objects.all()
                return render(req,'admindashboard.html',{'data':a_data , 'add_emp':True,'departments':departments})
            else:
                Add_Employee.objects.create(Name=en,Email=ee,Contact=ec,Dept=ed,Image=ei,Code=eco)
                messages.success(req,'Employee created')
                a_data= req.session.get('a_data')
                departments = Add_Employee.objects.all()
                return render(req,'admindashboard.html',{'data':a_data , 'add_emp':True,'departments':departments})
    else:
        return redirect('login')
    

@never_cache
def show_emp(req):
     if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        departments = Add_Employee.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'show_emp':True, 'departments':departments})
     else:
        return redirect('login')
     

@never_cache
def edit_emp(req, id):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        employee = Add_Employee.objects.get(id=id)
        departments = Department.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'edit_emp':True, 'employee':employee, 'departments':departments})
    else:
        return redirect('login')


@never_cache
def update_emp(req, id):
    if 'a_data' in req.session:
        if req.method == 'POST':
            employee = Add_Employee.objects.get(id=id)
            employee.Name = req.POST.get('name')
            employee.Email = req.POST.get('email')
            employee.Contact = req.POST.get('contact')
            employee.Dept = req.POST.get('dept')
            employee.Code = req.POST.get('code')
            if req.FILES.get('image'):
                employee.Image = req.FILES.get('image')
            employee.save()
            messages.success(req, 'Employee updated successfully')
        return redirect('show_emp')
    else:
        return redirect('login')

@never_cache
def delete_emp(req, id):
    if 'a_data' in req.session:
        employee = Add_Employee.objects.filter(id=id).first()
        if employee:
            employee.delete()
            messages.success(req, 'Employee deleted successfully')
        else:
            messages.warning(req, 'Employee not found')
        return redirect('show_emp')
    else:
        return redirect('login')
     
@never_cache
def emp_all_query(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        empallquery = Query.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'emp_all_query':True, 'all_query':empallquery})
    else:
        return redirect('login')
    
@never_cache
def reply(req , pk):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        q_data=Query.objects.get(id=pk)
        emp_all_query=Query.objects.all()
        return render(req, 'admindashboard.html', {'data':a_data , 'q_data':q_data , 'emp_all_query':emp_all_query} )

@never_cache
def a_reply(req , pk):
    if 'a_data' in req.session:
        q_old_data= Query.objects.get(id=pk)
        if req.method == 'POST':
            ar=req.POST.get('reply')
            q_old_data.Reply=ar
            q_old_data.Status="done"
            q_old_data.save()
        a_data = req.session.get('a_data')
        emp_all_query=Query.objects.all()
        return render(req, 'admindashboard.html', {'a_data':a_data  , 'emp_all_query':emp_all_query} )
    
@never_cache
def add_item(req):
    if 'a_data' in req.session:
        a_data=req.session.get('a_data')
        if req.method == "POST":
            name = req.POST.get('item_name')
            desc = req.POST.get('item_desc')
            price = req.POST.get('item_price')
            color = req.POST.get('item_color')
            category = req.POST.get('item_category')
            quantity = req.POST.get('item_quantity')
            image = req.FILES.get('item_image')

            if not name or not desc or not price or not category or not quantity:
                messages.warning(req, 'Please fill in all required item fields before adding the product.')
                return render(req,'admindashboard.html',{'data':a_data , 'add_item':True})

            Item.objects.create(
                item_name=name,
                item_desc=desc,
                item_price=price,
                item_color=color,
                item_category=category,
                item_quantity=quantity,
                item_image=image
            )
            messages.success(req, 'Item added successfully')
            return redirect('admindashboard')
        else:
            a_data=req.session.get('a_data')
            return render(req,'admindashboard.html',{'data':a_data , 'add_item':True})  
    else: 
        return redirect('login')

@never_cache
def show_item(req):
    if 'a_data' in req.session:
        a_data=req.session.get('a_data')
        all_items = Item.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'show_item':True , 'all_items':all_items})
    else:
        return redirect('login')
    
@never_cache
def show_users(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        all_users = User.objects.all()
        return render(req, 'admindashboard.html', {'data': a_data, 'show_users': True, 'all_users': all_users})
    else:
        return redirect('login')
    
@never_cache
def profile(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Add_Employee.objects.get(id=eid)
      return render(req,'empdashboard.html',{'data':emp_data , 'profile':True})
   return redirect('login')


#==========================================================================================================================================

#      Forgot Password Views

import random
def forgot(req):
    return render(req,'enteremail.html')

def enteremail(req):
    if req.method == 'POST':
        e = req.POST.get('email')
        user= User.objects.filter(Email=e)
        if not user:
            msg="please enter valid email"
            return render(req,'enteremail.html',{'msg':msg})
        else:
            otp = random.randint(100000,999999)
            req.session['otp'] = str(otp)   # ✅ string me store karo
            req.session['email']= e
            send_mail('otp from django server',
                      f'your forgot password otp is {otp}',
                      "from@gmail.com",
                      [e])
            return render(req,'changepass.html')
            
            

def reset(req):
    if req.method == 'POST':
        e_otp = req.POST.get('otp')
        n_pass = req.POST.get('password')
        c_pass = req.POST.get('cpassword')

        otp = req.session.get('otp')
        email = req.session.get('email')

        if not otp or not email:
            return render(req, 'enteremail.html', {'msg': 'Session expired!'})

        if str(otp) == str(e_otp):

            if n_pass == c_pass:
                userdata = User.objects.get(Email=email)

                # ✅ IMPORTANT
                userdata.Pass = n_pass.strip()
                userdata.CPass = c_pass.strip()
                userdata.save()

                req.session.flush()

                return redirect('login')

            else:
                return render(req, 'changepass.html', {'msg1': 'Password not matched'})

        else:
            return render(req, 'changepass.html', {'msg': 'Invalid OTP'})







#==========================================================================================================================================

       # User Dashboard Views



@never_cache
def userdashboard(req):
    cart_count = 0
    user = None
    if 'user_id' in req.session:
        user = User.objects.get(id=req.session['user_id'])
        cart_items = Cart.objects.filter(user=user)
        cart_count = sum(item.quantity for item in cart_items)
    
    items = Item.objects.all()
    return render(req,'userdashboard.html' ,{'items': items, 'cart_count': cart_count , 'user': user})



#==========================================================================================================================================

       # Employee Dashboard Views

@never_cache
def empdashboard(req):
    if 'emp_id' in req.session:
        emp_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=emp_id)
        return render(req,'empdashboard.html',{'data':emp_data})
    return redirect('login')


@never_cache
def setting(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Add_Employee.objects.get(id=eid)
      return render(req,'empdashboard.html',{'data':emp_data , 'setting':True})
   return redirect('login')

@never_cache
def query(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Add_Employee.objects.get(id=eid)
      departments = Department.objects.all()
      return render(req,'empdashboard.html',{'data':emp_data , 'query':True ,'emp_dept':departments })
   else:
      return redirect('login')
  
@never_cache
def querydata(req):
    if 'emp_id' in req.session:
      if req.method == 'POST':
         n=req.POST.get('name')
         e=req.POST.get('email')
         d=req.POST.get('department')
         q=req.POST.get('query')
         Query.objects.create(Name=n,Email=e,Dept=d,Query=q)
         messages.success(req,'Query submitted')
         eid = req.session.get('emp_id')
         emp_data = Add_Employee.objects.get(id=eid)
         departments = Department.objects.all()
         return render(req,'empdashboard.html',{'data':emp_data , 'query':True ,'emp_dept':departments })
    else:
        return redirect('login')



@never_cache
def allquery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        all_query = Query.objects.filter(Email=emp_data.Email)
        return render(req, 'empdashboard.html', {'data':emp_data,'allquery':True , 'all_query':all_query})
    else:
        return redirect('login')
    

@never_cache
def pendingquery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        all_query = Query.objects.filter(Email=emp_data.Email, Status="pending")
        return render(req, 'empdashboard.html', {'data':emp_data,'pendingquery':True , 'all_query':all_query})
    else:
        return redirect('login')
    
@never_cache
def donequery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        all_query = Query.objects.filter(Email=emp_data.Email, Status="done")
        return render(req, 'empdashboard.html', {'data':emp_data,'donequery':True , 'all_query':all_query})
    else:
        return redirect('login')


@never_cache
def edit_all_query(req, pk):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        old_querydata = Query.objects.get(id=pk)
        emp_dept = Department.objects.all()
        all_query = Query.objects.filter(Email=emp_data.Email)
        return render(req, 'empdashboard.html', { 'data': emp_data, 'allquery': True, 'old_querydata': old_querydata, 'emp_dept': emp_dept, 'all_query': all_query})
    else:
        return redirect('login')

@never_cache
def updated_query(req, pk):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        if req.method == 'POST':
            d = req.POST.get('department')
            q = req.POST.get('query')
            old_q_data = Query.objects.get(id=pk)
            old_q_data.Dept = d
            old_q_data.Query = q
            old_q_data.save()
            messages.success(req, "Query updated successfully")
            emp_data = Add_Employee.objects.get(id=e_id)
            all_query = Query.objects.filter(Email=emp_data.Email)
            return render(req, 'empdashboard.html', { 'data': emp_data, 'allquery': True, 'all_query': all_query})
    else:
        return redirect('login')
    


@never_cache
def emp_q_delete(req, id):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        q = Query.objects.filter(id=id).first()
        if q:
            q.delete()
            messages.success(req, "Query deleted successfully")
        else:
            messages.warning(req, "Query already deleted")
        return redirect('empdashboard')

    else:
        return redirect('login')



from django.db.models import Q 

@never_cache
def search(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        if req.method == 'POST':
          s=req.POST.get('search')

        #   all_query = Query.objects.filter(Email=emp_data.Email,Query=s)
        #   all_query = Query.objects.filter(Email__icontains=emp_data.Email,Query__icontains=s)
        #   all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains=s)
        #   all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains=s , Dept__icontains=s)
        #   all_query = Query.objects.filter(Email=emp_data.Email and (Q(Query__icontains=s) | Q(Dept__icontains=s)))
          all_query = Query.objects.filter(Email=emp_data.Email).filter(Q(Query__icontains=s) | Q(Dept__icontains=s))
          return render(req, 'empdashboard.html', {'data':emp_data, 'allquery':True , 'all_query':all_query ,'s':s})
   
    else:
        return redirect('login')
    

 
#========================================================================================================================================== 
    
      # Payment Views

import razorpay
@never_cache
def payment(req, pk):
    data = None
    if 'a_data' in req.session:
        data = req.session.get('a_data')
    elif 'user_id' in req.session:
        data = User.objects.get(id=req.session.get('user_id'))
    elif 'emp_id' in req.session:
        data = Add_Employee.objects.get(id=req.session.get('emp_id'))
    item_detail = Item.objects.get(id=pk)
    return render(req,'payment.html', {'item_detail': item_detail, 'data': data})



@never_cache
def pay_amount(req,pk):
    if req.method == 'POST':
        amount1 = req.POST.get('itemprice')
        amount = int(amount1) * 100
        client = razorpay.Client(auth =("rzp_test_pr99iascS1WRtU" , "UTDIzPGwICnAssu3Q3lk7zUi"))
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        data = None
        if 'a_data' in req.session:
            data = req.session.get('a_data')
        elif 'user_id' in req.session:
            data = User.objects.get(id=req.session.get('user_id'))
        elif 'emp_id' in req.session:
            data = Add_Employee.objects.get(id=req.session.get('emp_id'))
        item_detail = Item.objects.get(id=pk)
        Order.objects.create(
            order_id=payment.get('id'),
            amount=int(amount1)
        )
        return render(req, 'payment.html', {'payment': payment, 'amount': amount1 , 'data':data , 'item_detail':item_detail})
    

@never_cache
def pay_status(req, pk):
    print(req.POST)
    rpi=req.POST.get('razorpay_payment_id')
    roi=req.POST.get('razorpay_order_id')
    old_roi = Order.objects.get(order_id=roi)
    old_roi.razorpay_id = rpi
    old_roi.status = True
    old_roi.save()
    return render(req,'success.html', {'order': old_roi})


#==========================================================================================================================================

  # Cart Views

def add_to_cart(req, id):
    if 'user_id' in req.session:
        user = User.objects.get(id=req.session['user_id'])
        item = Item.objects.get(id=id)

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            item=item
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('userdashboard')
    else:
        return redirect('login')




def cart_page(req):
    if 'user_id' in req.session:
        user = User.objects.get(id=req.session['user_id'])
        cart = Cart.objects.filter(user=user)

        total = 0
        for i in cart:
            total += i.item.item_price * i.quantity

        return render(req,'cart.html',{
            'cart':cart,
            'total':total
        })



def remove_cart(req,id):
    Cart.objects.get(id=id).delete()
    return redirect('cart_page')