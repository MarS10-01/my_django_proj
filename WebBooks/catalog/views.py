from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Author, BookInstance, Genre
from .forms import AuthorsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, 'catalog/authors_add.html',
                  {'form': authorsform, 'author': author})


def create(request):
    if request.method == 'POST':
        author = Author()
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')

def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect('/authors_add')
    except Author.DoesNotExist:
        return HttpResponseNotFound('<h2>Автор не найден</h2>')

def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')
    else:
        return render(request, 'catalog/edit1.html', context={'author': author})

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='4').order_by('due_back')



class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        instance = BookInstance.objects.filter(book=book, status_id=1).first()
        if instance and request.user.is_authenticated:
            instance.status_id = 4
            instance.borrower = request.user
            instance.due_back = request.POST.get('due_back')
            instance.save()

        return redirect('book-detail', pk=book.pk)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4
def magazine(request):
    return HttpResponse('<iframe src="https://yandex.ru/map-widget/v1/?um=constructor%3A8c0236a73e8e454d598deed3b07517c8fe404d1544d25d8fba15af350c2a57ed&amp;source=constructor" width="100%" height="400" frameborder="0"></iframe>')

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instance_available = BookInstance.objects.filter(status__exact = 4).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instance_available': num_instance_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits})

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

