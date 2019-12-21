from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.views.generic import (
  ListView,
  DetailView,
  CreateView,
  DeleteView,
)

from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import Book, BookCopy
from .forms import CreateBookCopyForm

class UserOwnsBookCopyMixin(UserPassesTestMixin):
  def test_func(self):
    bookcopy_id = self.kwargs['bookcopy_id']
    return BookCopy.objects.filter(
      owner_id=self.request.user.id, id=bookcopy_id,
    ).exists()

class BookCopyIndex(ListView, LoginRequiredMixin):
  model = BookCopy
  context_object_name = 'bookcopies'
  template_name = 'books/bookcopy_index.html'

  def get_queryset(self):
    return super().get_queryset().filter(owner=self.request.user).select_related('book')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['create_form'] = CreateBookCopyForm()
    context['create_url'] = reverse('add-bookcopy')
    return context

class BookCopyCreate(View, LoginRequiredMixin):
  def post(self, request):
    form = CreateBookCopyForm(request.POST)
    if not form.is_valid():
      return render(request, 'books/bookcopy_index.html', {'form': form})
    isbn = form.cleaned_data['isbn']
    book, _created = Book.objects.get_or_create(isbn=isbn)
    book.copies.create(owner=request.user)
    messages.success(request, 'Book created')
    return HttpResponseRedirect(reverse('my-bookcopies'))


class BookCopyDetail(DetailView):
  model = BookCopy
  context_object_name = 'bookcopy'
  template_name = 'books/bookcopy_detail.html'
  pk_url_kwarg = 'bookcopy_id'

  def get_queryset(self):
    return super().get_queryset().select_related('book')

class BookCopyDelete(DeleteView, UserOwnsBookCopyMixin):
  model = BookCopy
  success_url = reverse_lazy('my-bookcopies')
  pk_url_kwarg = 'bookcopy_id'
