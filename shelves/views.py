from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.db.models import Prefetch
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Shelf, Shelving
from .authorization import UserOwnsShelfMixin, UserOwnsShelvingMixin
from .forms import CreateShelfForm, CreateShelvingForm
from books.models import BookCopy


class ShelfIndex(ListView, LoginRequiredMixin):
    model = Shelf
    context_object_name = "shelves"
    template_name = "shelves/shelf_index.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = CreateShelfForm()
        context["create_url"] = reverse("shelf-create")
        return context


class ShelfDetail(DetailView):
    queryset = Shelf.objects.prefetch_related(
        Prefetch("book_copies", queryset=BookCopy.objects.select_related("book"))
    )
    context_object_name = "shelf"
    template_name = "shelves/shelf_detail.html"
    pk_url_kwarg = "shelf_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id == context["shelf"].owner_id:
            context["add_url"] = reverse(
                "shelving-create", kwargs={"shelf_id": self.kwargs["shelf_id"]}
            )
            context["books"] = [bc.book for bc in context["shelf"].book_copies.all()]
            context["unshelved_books"] = (
                BookCopy.objects.filter(owner_id=self.request.user.id)
                .exclude(id__in=[b.id for b in context["shelf"].book_copies.all()])
                .select_related("book")
            )
        return context


class ShelfCreate(CreateView, LoginRequiredMixin):
    model = Shelf
    form_class = CreateShelfForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ShelfDelete(DeleteView, UserOwnsShelfMixin):
    model = Shelf
    success_url = reverse_lazy("my-shelves")
    pk_url_kwarg = "shelf_id"


class ShelvingCreate(CreateView, UserOwnsShelfMixin):
    model = Shelving
    form_class = CreateShelvingForm

    def get_success_url(self):
        return reverse("shelf-detail", kwargs={"shelf_id": self.object.shelf_id})

    def form_valid(self, form):
        form.instance.shelf_id = self.kwargs["shelf_id"]
        return super().form_valid(form)


class ShelvingDelete(DeleteView, UserOwnsShelfMixin):
    model = Shelving
    pk_url_kwarg = "shelving_id"

    def get_success_url(self):
        return reverse(
            "shelf-detail", kwargs={"shelf_id": self.request.kwargs["shelf_id"]}
        )

