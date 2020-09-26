from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms import inlineformset_factory

from .models import Question, Choice
from .forms import *

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """Return the last five published questions
           (not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
def new_poll(request, question_id):
    q = Question.objects.get(pk=question_id)
    QuestionFormset = inlineformset_factory(Question, Choice, fields=('choice_text'),)
    tmpl_vars = {
        'form': QuestionForm(),
        'form2': ChoiceForm(),
    }
    
    formset = QuestionFormset() # when a url is called initially it is GET method so you have to send a instance of form first (empty form)
    if request.method == 'POST':
        formset = QuestionFormset(request.POST or None, instance=question)
        if formset.is_valid():
            new_poll = formset.save(commit=False)
            new_poll.pub_date = timezone.localtime(timezone.now())
            new_poll.save()
            return redirect('polls:index', question_id=question.id)
        else:
            formset = QuestionFormset() # this will return the errors in your form
            
    return render(request, 'polls/new.html', {'formset':formset})
