from django.shortcuts import render, redirect
from .models import Project
from django.db.models import Q
from .forms import ContactForm


def project_index(request):
    projects = Project.objects.all()

    query = request.GET.get('q')
    if query:
        projects = Project.search(query)

    return render(request, 'projects/project_index.html', {'projects': projects})


def about(request):
    return render(request, 'projects/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Handle successful form submission. 
            # For now, we'll just print the data.
            print(form.cleaned_data)
            return redirect('project_index')  # Redirect to the homepage after submission
    else:
        form = ContactForm()
    return render(request, 'projects/contact.html', {'form': form})


def search_results(request):
    query = request.GET.get('q', '')
    if query:
        projects = Project.search(query)
    else:
        projects = Project.objects.none()  # Returns an empty queryset
    return render(request, 'projects/search_results.html', {'projects': projects})
