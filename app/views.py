from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import DesignRequest, Category
from .forms import DesignRequestForm, CategoryForm
from django import forms


@login_required
def design_request_create(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.status = 'new'
            design_request.save()
            return redirect('design_request_detail', pk=design_request.pk)
    else:
        form = DesignRequestForm()
        form.fields['status'].widget.attrs['disabled'] = True
        if not request.user.is_superuser:
            form.fields['status'].widget = forms.HiddenInput()
            form.fields['image_after'].widget = forms.HiddenInput()
            form.fields['comment'].widget = forms.HiddenInput()
    return render(request, 'design/design_request_form.html', {'form': form, "action": "create"})


@login_required
def design_request_edit(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk)
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            design_request = form.save(commit=False)
            if design_request.status == 'in_progress' and not design_request.comment:
                form.add_error('comment', 'При изменении статуса на "В процессе работы" нужно указать комментарий.')
            elif design_request.status == 'completed' and not design_request.image_after:
                form.add_error('image_after', 'При изменении статуса на "Сделано" необходимо прикрепить изображение.')
            else:
                design_request.save()
                return redirect('design_request_detail', pk=design_request.pk)
    else:
        if not request.user.is_superuser:
            form = DesignRequestForm(instance=design_request, initial={'status': design_request.status})
            form.fields['status'].widget = forms.HiddenInput()
            form.fields['image_after'].widget = forms.HiddenInput()
            form.fields['comment'].widget = forms.HiddenInput()
        else:
            form = DesignRequestForm(instance=design_request)
            if design_request.status == 'new':
                form.fields['status'].choices = [("in_progress", "В процессе работы"), ("completed", "Сделано")]
            elif design_request.status == 'in_progress':
                form.fields['status'].choices = [("completed", "Сделано"),]
                
    return render(request, 'design/design_request_form.html', {'form': form, "action": "edit"})    


@login_required
def design_request_delete(request, pk):
    if request.user.is_superuser:
        design_request = get_object_or_404(DesignRequest, pk=pk)
    else:
        design_request = get_object_or_404(DesignRequest, pk=pk, user=request.user)

    design_request.delete()
    return redirect('design_request_list', username=request.user.username)


@login_required
def design_request_list(request, username=None):
    status = request.GET.get("status")
    user = get_object_or_404(User, username=request.user.username)
    
    if user.is_superuser:
        design_requests = DesignRequest.objects.all()
        context = { 'design_requests': design_requests }
        
        if status:
            design_requests = DesignRequest.objects.filter(status=status).order_by("created_at")
            context = { 'design_requests': design_requests, "status": status }
            
        if username:
            user = get_object_or_404(User, username=username)
            design_requests = DesignRequest.objects.filter(user=user)
            context = { 'design_requests': design_requests, "status": status }
        
        return render(request, 'design/user_design_requests.html', context)
    
    else:
        design_requests = DesignRequest.objects.filter(user=user)
        len_design_request = DesignRequest.objects.filter(user=user).count()
        context = { 'design_requests': design_requests }
    
        if request.GET.get("sort") and request.GET.get("filter"):
            query = request.GET.get("filter")
            design_requests = DesignRequest.objects.filter(user=user, status="completed").order_by("created_at")[:4]
            design_request_count = DesignRequest.objects.filter(user=user, status="in_progress").count()
            len_design_request = DesignRequest.objects.filter(user=user, status="completed").count()
    
            context = { 'design_requests': design_requests, "query": query, "design_request_count": design_request_count, "page": "home", "len_design_request": len_design_request }
        
        if status:
            design_requests = design_requests = DesignRequest.objects.filter(user=user, status=status).order_by("created_at")
            context = { 'design_requests': design_requests, "status": status }
    
        return render(request, 'design/user_design_requests.html', context)


@login_required
def design_request_detail(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk)
    return render(request, 'design/design_request_detail.html', {'design_request': design_request})
    


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form, "action": "create"})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form, "action": "edit"})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'category/category_detail.html', {'category': category})

    