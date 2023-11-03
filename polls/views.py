from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PollForm, ChoiceForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import *
from django.db.models import Sum
from django.template import TemplateDoesNotExist
from django.contrib import messages 

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('polls:index')
    else:
        form = SignUpForm()
    return render(request, 'poll/signup.html', {'form': form})


def user_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('polls:index')
            else:
                return render(request, 'poll/login.html', {'error': 'Invalid credentials. Please try again.'})
        else:
            return render(request, 'poll/login.html')
    except TemplateDoesNotExist:
        return HttpResponse("Login template is missing.")


def user_logout(request):
    logout(request)
    return render(request, 'poll/logout.html')

@login_required
def create_poll(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(x))
                        for x in range(3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            poll = poll_form.save(commit=False)
            poll.creator = request.user
            poll.save()
            for choice_form in choice_forms:
                choice = choice_form.save(commit=False)
                choice.poll = poll
                choice.save()
            return redirect('polls:index')
    else:
        poll_form = PollForm()
        choice_forms = [ChoiceForm(prefix=str(x)) for x in range(3)]
    return render(request, 'poll/create_poll.html', {'poll_form': poll_form, 'choice_forms': choice_forms})

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:10]
    context = {'latest_poll_list': latest_poll_list}
    for poll in latest_poll_list:
        poll.choices_with_votes = poll.choice_set.annotate(
            total_votes=Sum('votes'))
    return render(request, 'poll/index.html', context)

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'poll/detail.html', {'poll': poll})


from datetime import datetime

from django.utils.timezone import make_aware

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = poll.choice_set.all()
    total_votes = sum(choice.votes for choice in choices)

    current_time = timezone.localtime(timezone.now())

    is_voting_closed = current_time > poll.end_date

    context = {
        'poll': poll,
        'choices': choices,
        'total_votes': total_votes,
        'is_voting_closed': is_voting_closed,
    }

    return render(request, 'poll/results.html', context)


@login_required 
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    current_time = timezone.now()

    if current_time > poll.end_date:
        messages.warning(request, "Voting is closed for this poll.")
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))

    user = request.user
    if Vote.objects.filter(user=user, poll=poll).exists():
        messages.warning(request, "You have already voted.")
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))

    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return render(request, 'poll/detail.html', {'poll': poll})

    selected_choice.votes += 1
    selected_choice.save()
    Vote.objects.create(user=user, poll=poll, choice=selected_choice)

    messages.success(request, "Your vote has been recorded.")
    return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))

