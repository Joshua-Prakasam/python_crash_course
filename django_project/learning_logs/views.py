from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """The Home page for Learning Log"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('learning_logs:topics'))
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Show all topics."""
    all_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': all_topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    content = Topic.objects.get(id=topic_id)
    check_topic_owner(content, request)
    entries = content.entry_set.order_by('-date_added')
    context = {'topic': content, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            create_topic = form.save(commit=False)
            create_topic.owner = request.user
            create_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic_content = Topic.objects.get(id=topic_id)
    check_topic_owner(topic_content, request)

    if request.method != 'POST':
        # No data submitted; create a blank form
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            add_entry = form.save(commit=False)
            add_entry.topic = topic_content
            add_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic_content, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic_content = entry.topic
    check_topic_owner(topic_content, request)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_content.id]))

    context = {'entry': entry, 'topic': topic_content, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(topic_content, request):
    # Make sure the topic belongs to the current user.
    if topic_content.owner != request.user:
        raise Http404
