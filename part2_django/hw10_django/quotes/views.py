from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Author, Quote, Tag

from .forms import AuthorForm, QuoteForm, TagForm


def home(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    top_tags = Quote.objects.values('tags__name').annotate(quote_count=Count('tags__name')).order_by('-quote_count')[
               :10]
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page, 'top_tags': top_tags})


def author_about(request, _id):
    author = Author.objects.get(pk=_id)
    return render(request, 'quotes/author.html', context={'author': author})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            return redirect(to='quotes:home')
        else:
            return render(request, 'quotes/add_quote.html',
                          context={'form': form, 'message': "Incorrect form"})
    return render(request, 'quotes/add_quote.html', context={'form': QuoteForm()})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:home')
        else:
            return render(request, 'quotes/add_author.html',
                          context={'form': AuthorForm, 'message': "Форма невірна"})
    return render(request, 'quotes/add_author.html', context={'form': AuthorForm()})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return redirect(to='quotes:home')
        else:
            return render(request, 'quotes/add_tag.html',
                          context={'form': TagForm, 'message': "Incorrect form"})
    return render(request, 'quotes/add_tag.html', context={'form': TagForm})


def find_tag(request, _id):
    per_page = 10
    if isinstance(_id, int):
        quotes = Quote.objects.filter(tags=_id).all()
    elif isinstance(_id, str):
        tag_id = Tag.objects.filter(name=_id).first()
        quotes = Quote.objects.filter(tags=tag_id).all()
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    top_tags = Quote.objects.values('tags__id', 'tags__name').annotate(quote_count=Count('tags__name')).order_by(
        '-quote_count')[:10]

    return render(request, 'quotes/find_tag.html',
                  context={'quotes': page_obj, 'tag_name': _id, 'top_tags': top_tags})
