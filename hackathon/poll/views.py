from django.shortcuts import render,redirect,HttpResponse
from .models import Poll,Result,Comment
from .forms import  PollForm


def poll_list(request):
    polls = Poll.objects.all().order_by('-created_date')[:10]
    ret = {'polls':polls}

    return render(request,'poll/poll_list.html',ret)

def poll_edit(request):
    if request.method =='GET':
        form = PollForm()
        return render(request,'poll/poll_edit.html',{'form':form})
    elif request.method=='POST':
        form =PollForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            notification = form.cleaned_data['notification']
            author = request.user
            Poll.objects.create(title=title,
                                notification=notification,
                                author=author)
        else:
            return render(request, 'poll/poll_edit.html',{'form':form})
        return redirect('poll:poll_list')


def poll_detail(request,poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method=='POST':
        if request.POST['radio']:
            value = request.POST['radio']
            comment = request.POST['comment']
            print(value)
            Result.objects.create(
                student=request.user,
                poll=poll,
                score=value
            )
            Comment.objects.create(
                student=request.user,
                poll=poll,
                text=comment

            )
            return redirect('poll:poll_result',poll_id=poll_id)
        else:
            return redirect('poll:poll_detail',poll_id=poll.pk)
    elif request.method=="GET":
        context = {}
        context['poll']=poll
        return render(request,'poll/poll_detail.html',context)

def poll_result(request,poll_id):

    poll = Poll.objects.get(pk=poll_id)
    result1 = Result.objects.filter(poll=poll,score=1)
    result2 = Result.objects.filter(poll=poll,score=2)
    result3 = Result.objects.filter(poll=poll,score=3)
    result4 = Result.objects.filter(poll=poll,score=4)
    result5 = Result.objects.filter(poll=poll,score=5)
    comments = Comment.objects.filter(poll=poll)
    results = Result.objects.filter(poll=poll)
    context = {}
    context['poll'] = poll
    context['result1'] = result1
    context['result2'] = result2
    context['result3'] = result3
    context['result4'] = result4
    context['result5'] = result5
    context['results'] = results
    average = (result1.count() + result2.count()*2 + result3.count()*3 + result4.count()*4 + result5.count()*5)/results.count()
    context['average'] = average
    context['comments'] = comments

    return render(request, 'poll/poll_result.html',context)



