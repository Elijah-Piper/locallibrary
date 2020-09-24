from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
	"""View function for home page of the site."""

	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# The 'all()' is implied by default
	num_authors = Author.objects.count()

	num_fiction = Genre.objects.filter(name__icontains='fiction').count()
	num_nonfiction = num_books - num_fiction

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_fiction': num_fiction,
		'num_nonfiction': num_nonfiction,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
	model = Book