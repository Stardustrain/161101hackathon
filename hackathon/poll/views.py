from django.shortcuts import render, redirect, HttpResponse
from .models import Poll, Result, Comment, Like
import json
from .forms import PollForm


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


def poll_result(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    ret = [
        Result.objects.filter(poll=poll,
                              score=i).count()
        for i in range(1, 6)
    ]

    tot = 0
    for ind, num in enumerate(ret):
        tot += (ind+1) * num

    student = Result.objects.filter(poll_id=poll_id).count()
    avg = tot/student

    comments = Comment.objects.filter(poll=poll)

    context = {'score': ret,
               'avg': avg,
               'comments': comments,
               'poll': poll}

    return render(request, 'poll/poll_result.html', context)


def like(request, com_id):
    like = Like.objects.get(comment=com_id)
    com = Comment.objects.get(comment=com_id)
    like.objects.add(sudent=request.user, comment=com)


