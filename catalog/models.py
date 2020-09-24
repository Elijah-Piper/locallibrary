from django.db import models
from django.urls import reverse
import uuid


class Genre(models.Model):
	"""Model defining book genres."""
	name = models.CharField(
		max_length=200, 
		help_text='Enter a book genre (e.g. Science Fiction)'
	)

	def __str__(self):
		"""String representation for a Genre instance."""
		return self.name


class Book(models.Model):
	"""Model defining a book (but not a specific copy)."""
	title = models.CharField(max_length=200)

	# ForeignKey used because book can only have one author, but authors can have multiple books.
	# Author as a string rather than an object because it hasn't been declared yet in the file.
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

	summary = models.TextField(
		max_length=1000, 
		help_text='Enter a brief description of the book'
	)
	isbn = models.CharField(
		'ISBN', 
		max_length=13, 
		help_text='12 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
	)

	# ManyToManyField used because genre can contain many books. Books can cover many genres.
	# Genre clas has already been defined so we can specify the object above.
	genre = models.ManyToManyField(
		Genre, 
		help_text='Select a genre for this book'
	)

	def __str__(self):
		"""String representation for a book instance."""
		return self.title

	def get_absolute_url(self):
		"""Returns the URL to access a detail record for this book."""
		return reverse('book-detail', args=[str(self.id)])

	def display_genre(self):
		"""Returns a string for the genre; it's required for Admin list display."""
		return ', '.join(genre.name for genre in self.genre.all()[:3])

	display_genre.short_description = 'Genre'

class BookInstance(models.Model):
	"""A model representing individual book copies."""
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		help_text='Unique ID for this particular book across the whole library'
	)
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)

	LOAN_STATUS = (
		('m', 'Maintenace'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)

	status = models.CharField(
		max_length=1,
		choices=LOAN_STATUS,
		blank=True,
		default='m',
		help_text='Book availability'
	)

	class Meta:
		ordering = ['due_back']

	def __str__(self):
		"""String representation of each book instance record."""
		return f'{self.id} ({self.book.title})'


class Author(models.Model):
	"""Model representing book author records."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('Died', null=True, blank=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		"""Returns the absolute URL to access a particular author instance."""
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		"""String representation of an instance of an author record."""
		return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
	"""Model representing languages which books can be printed in."""
	name = models.CharField(
		max_length=100, 
		help_text="Enter the language the book is printed in")

	def __str__(self):
		"""String representation for a printing language."""
		return f'{self.name}'

	def get_absolute_url(self):
		"""Returns the absolute URL to access a particular language section."""
		return reverse('language-detail', args=[str(self.name)])