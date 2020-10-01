from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
	"""View function for home page of the site."""

	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# The 'all()' is implied by default
	num_authors = Author.objects.count()

	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	num_fiction = Genre.objects.filter(name__icontains='fiction').count()
	num_nonfiction = num_books - num_fiction

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_fiction': num_fiction,
		'num_nonfiction': num_nonfiction,
		'num_visits': num_visits,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
	model = Book
	paginate_by = 50

class BookDetailView(generic.DetailView):
	model = Book


class AuthorListView(generic.ListView):
	model = Author
	paginate_by = 50

class AuthorDetailView(generic.DetailView):
	model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to the current user."""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
	"""Generic class-based view listing all loaned books for librarian users."""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_all_borrowed.html'
	#paginate_by = 10

	permission_required = 'catalog.can_mark_returned'

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')