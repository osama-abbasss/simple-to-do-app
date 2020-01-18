from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ToDoForm
from .models import ToDo


@login_required
def add_to_do(request):
    user = request.user

    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            status = form.cleaned_data.get('status')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')

            to_do = ToDo(
            user= user,
            title= title ,
            content= content ,
            date= date ,
            time= time ,
            )
            to_do.save()
            if status:
                to_do.status =True
                to_do.save()
            return redirect('to_do:to_do_list')
        else:
            print('error')

    else:
        form = ToDoForm()

    template_name = 'to_do/add_to_do.html'
    context = {'form':form}

    return render(request, template_name, context)


class ToDoList(LoginRequiredMixin, ListView):
    model = ToDo
    template_name = 'to_do/to_do_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user = self.request.user)


def status_true(request, slug):
    to_do = ToDo.objects.get(user= request.user, slug=slug)
    to_do.status = True
    to_do.save()
    return redirect('to_do:to_do_list')

def status_false(request, slug):
    to_do = ToDo.objects.get( user= request.user ,slug=slug)
    to_do.status = False
    to_do.save()
    return redirect('to_do:to_do_list')

@login_required
def update(request, slug):
    model = ToDo.objects.get(user=request.user, slug=slug)
    if request.method == 'POST':
        form = ToDoForm(request.POST,instance=model)
        if form.is_valid():
            form.save()
            return redirect('to_do:to_do_list')
        else:
            print('error')
    else:
        form = ToDoForm(instance=model)

    template_name = 'to_do/update.html'
    context = {'form':form}
    return render(request, template_name, context)



class Delete(LoginRequiredMixin,DeleteView):
    model = ToDo
    success_url = reverse_lazy('to_do:to_do_list')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(user = self.request.user)


@login_required
def delete(request, slug):
    model = ToDo.objects.get(user= request.user, slug=slug)
    model.delete()
    return redirect('to_do:to_do_list')


@login_required
def detail_view(request, slug, username):
    try:
        object = ToDo.objects.get(user= request.user, slug=slug, user__username= username)
    except :
        return redirect('to_do:to_do_list')

    template_name= 'to_do/detail.html'
    context= {'object':object}

    return render(request, template_name, context)
