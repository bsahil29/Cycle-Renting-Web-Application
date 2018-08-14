import string
import random
from django.http import HttpResponse,Http404
from django.template import loader,RequestContext
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import users,cycles,session,cycleRequests
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def isLoggedin(request):
	session_id=''
	if 'csrftoken' in request.COOKIES:
		session_id = request.COOKIES['csrftoken']
	if session.objects.filter(session_id=session_id).exists():
		return session.objects.get(session_id=session_id).roll_no
	else:
		return -1

def signup(request):
	if isLoggedin(request)==-1:	
		if request.method == 'POST':
			name = request.POST.get("name")
			password = request.POST.get("password")
			roll_no = request.POST.get("roll_no")
			room = request.POST.get("room")
			hostel = request.POST.get("hostel")
			mobile_no = request.POST.get("mobile_no")
			email = request.POST.get("email")
			if users.objects.filter(roll_no=roll_no).exists():
				return render(request, 'polls/signup.html',{'info':'User exists!'})
			q = users(name = name,roll_no = roll_no,mobile_no = mobile_no,email = email,password = password,hostel = hostel,room_no = room)	
			q.save()
			return redirect("/polls/signin",{'info': 'Registration Successful'})
		else:
			return render(request, 'polls/signup.html',{'info':''})
	else:
		return profile(request)

def signin(request):
	if isLoggedin(request)==-1:
		if request.method == 'POST':
			roll_no = request.POST.get("roll_no")
			password = request.POST.get("password")
			if users.objects.filter(roll_no=roll_no).exists():
				person = users.objects.get(pk=roll_no)
				if person.password == password:
					session_id=''
					if 'csrftoken' in request.COOKIES:
						session_id = request.COOKIES['csrftoken']
					q = session(session_id=session_id,roll_no=roll_no)
					q.save()
					return profile(request)
				else:
					return render(request, 'polls/signin.html',{'info':'Password is incorrect!'})
			else:
				return render(request, 'polls/signin.html',{'info':'User does not exists!'})
		else:
			return render(request, 'polls/signin.html',{'info':''})	
	else:
		return profile(request)

def profile(request):
	if isLoggedin(request)!=-1:
		username = users.objects.get(pk=isLoggedin(request)).name
		myAcceptNotifications = []
		myRejectNotifications = []
		q = cycleRequests.objects.all()
		for x in q:
			if x.taker == isLoggedin(request):
				if x.status == 1:
					temp={}
					temp['name'] = cycles.objects.get(pk=x.cycle).roll_no.name
					temp['cycle_brand']	= cycles.objects.get(pk=x.cycle).cycle_brand
					temp['mobile_no']= cycles.objects.get(pk=x.cycle).roll_no.mobile_no
					myAcceptNotifications.append(temp)
				elif x.status == 2:	
					temp={}
					temp['name'] = cycles.objects.get(pk=x.cycle).roll_no.name
					temp['cycle_brand']	= cycles.objects.get(pk=x.cycle).cycle_brand
					myRejectNotifications.append(temp)

		q=cycles.objects.all()
		print(q)
		requestedCycles=[]
		notRequestedCycles=[]
		for x in q:
			if x.available == 0:
				continue
			# print(x.roll_no.roll_no)
			# print("----------------------")
			if x.roll_no.roll_no==isLoggedin(request):
				# print("My Cycle :" + x.cycle_brand + "is locked+++++++++++++++==")
				continue
			temp={}
			temp['id']=x.id
			temp['cycle_brand']=x.cycle_brand
			temp['cycle_description']=x.cycle_description
			temp['cycle_type']=x.cycle_brand
			temp['roll_no']=x.roll_no.roll_no
			temp['mobile_no']=x.roll_no.mobile_no
			temp['name']=x.roll_no.name
			temp['hostel']=x.roll_no.hostel
			temp['room_no']=x.roll_no.room_no
			l = cycleRequests.objects.all()
			isreq=0
			for l1 in l:
				if l1.cycle == x.id and l1.taker == isLoggedin(request) and l1.status==0:
					isreq=1
					break
			if isreq==1:
				requestedCycles.append(temp)
			else:
				notRequestedCycles.append(temp)
		# return render(request,'polls/profile.html',{'cyclesList':requestedCycles})
		r=cycleRequests.objects.all()
		brr=[]
		# i=1
		for y in r :
			# print("------------------------------------------")
			# print(y.cycle)

			roll_no=y.taker
			id_cycle=y.cycle
			isAcceptedAlready=0
			for w in r:
				if w.cycle == id_cycle and w.status == 1:
					isAcceptedAlready = 1
					break
			if isAcceptedAlready == 0 and y.status == 0:
				if isLoggedin(request)==cycles.objects.get(pk=id_cycle).roll_no.roll_no:
					temp={}
					temp['id']=cycleRequests.objects.get(cycle=id_cycle,taker=y.taker).id
					temp['cycle_brand']=cycles.objects.get(pk=id_cycle).cycle_brand
					temp['cycle_type']=cycles.objects.get(pk=id_cycle).cycle_type
					temp['roll_no']=roll_no
					temp['name']=users.objects.get(pk=roll_no).name
					temp['mobile_no']=users.objects.get(pk=roll_no).mobile_no
					brr.append(temp)
		return render(request,'polls/profile.html',{'username':username,'requestedCycles':requestedCycles,'notRequestedCycles':notRequestedCycles,'requestList':brr,'myAcceptNotifications':myAcceptNotifications,'myRejectNotifications':myRejectNotifications})
	else:
		return signin(request)

def registerCycle(request):
	if isLoggedin(request)!=-1:
		if request.method == 'POST':
			roll_no = isLoggedin(request)
			cycle_brand = request.POST.get("cycle_brand")
			cycle_type = request.POST.get("cycle_type")
			cycle_description = request.POST.get("cycle_description")
			q= users.objects.get(pk=roll_no)
			q.cycles_set.create(cycle_brand=cycle_brand,cycle_type=cycle_type,cycle_description=cycle_description,available = 1)
			return profile(request)
		else:
			return render(request, 'polls/registerCycle.html',{'info':''})
	else:
		return signin(request)		

def myCycleStatus(request):
	if isLoggedin(request)!=-1:
		# q=cycles.objects.filter(available=1)
		# q=cycles.objects.filter(available=1)
		roll = isLoggedin(request)
		q=cycles.objects.all()
		#u=users.objects.all()
		freeCycles=[]
		lockedCycles=[]
		for x in q:
			if x.roll_no.roll_no != isLoggedin(request):
				continue
			temp={}
			temp['id']=x.id
			temp['cycle_brand']=x.cycle_brand
			temp['cycle_type']=x.cycle_type
			temp['available'] = x.available
			# temp['name'] = x.roll_no.name
			# temp['roll_no'] = x.roll_no.roll_no
			# temp['mobile_no'] = x.roll_no.mobile_no
			if x.available == 0:
				lockedCycles.append(temp)
			else:
				freeCycles.append(temp)
		return render(request,'polls/myCycleStatus.html',{'freeCycles':freeCycles,'lockedCycles':lockedCycles})
	else:
		return signin(request)


def makeAvailable(request):
	if isLoggedin(request)!=-1:
		if request.method == 'POST':
			cycle_id = request.POST.get("id")
			q = cycles.objects.get(pk = cycle_id)
			q.available = 1
			q.save()
			return myCycleStatus(request)
		else:
			return myCycleStatus(request)	
	else:
		return signin(request)

def makenotAvailable(request):
	if isLoggedin(request)!=-1:
		if request.method == 'POST':
			cycle_id = request.POST.get("id")
			# roll_no = isLoggedin(request)
			q = cycles.objects.get(pk = cycle_id)
			q.available = 0
			q.save()
			return myCycleStatus(request)
		else:
			return myCycleStatus(request)	
	else:
		return signin(request)


def signout(request):
	session_id=''
	if 'csrftoken' in request.COOKIES:
		session_id = request.COOKIES['csrftoken']

	if session.objects.filter(session_id=session_id).exists():
		w = cycleRequests.objects.all()
		for t in w:
			if isLoggedin(request) == t.taker and t.status!=0:
				t.delete()
		q = session.objects.get(session_id=session_id)
		q.delete()
	return signin(request)

def requestCycle(request):
	# print("here--------------------------------")
	if isLoggedin(request)!=-1:
		if request.method == 'POST':
			cycle_id = request.POST.get("id")
			roll_no = isLoggedin(request)
			temp = cycleRequests.objects.all()
			for i in temp:
				# print(i.taker)
				# print(i.cycle)
				# print(roll_no)
				# print(cycle_id)
				if i.taker == roll_no and i.cycle==int(cycle_id):
					# print("out of here---------------------")
					return profile(request)	
			# if cycleRequests.objects.filter(taker=roll_no,cycle=id).exists():
			q = cycleRequests(taker=roll_no,cycle=cycle_id,status=0)
			q.save()
			return profile(request)
		else:
			return profile(request)
	else:
		return signin(request)

def approveRequest(request):
	if isLoggedin(request)!=-1:
		if request.method=='POST':
			# print('here-------------')
			reqId = request.POST.get("id")
			t = cycleRequests.objects.get(pk=reqId)
			t.status = 1
			t.save()
			t = cycles.objects.get(pk=cycleRequests.objects.get(pk=reqId).cycle)
			t.available = 0
			t.save()
			return profile(request)
		else:
			return profile(request)
	else:
		return signin(request)

def rejectRequest(request):
	if isLoggedin(request)!=-1:
		if request.method=='POST':
			reqId = request.POST.get("id")
			t = cycleRequests.objects.get(pk=reqId) 
			t.status = 2 #rejected status
			t.save()
			return profile(request)
		else:
			return profile(request)
	else:
		return signin(request)
