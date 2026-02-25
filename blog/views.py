from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse#, http404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.contrib import messages

from .forms import TicketForm, CommentForm, PostForm, PostSearch
from . models import *
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models.functions import Greatest

# Create your views here.

def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.slug = slugify(post.title, allow_unicode=True)
                post.reading_time = 0
                post.save()
                messages.success(request, 'Your post was successfully posted')
                return redirect('/blog')
        else:
            messages.error(request, 'You are not logged in')
            return redirect('/blog')
    else:
        form = PostForm()
    context={'form':form}
    return render(request, "blog/index.html", context)



#    return HttpResponse("Hello, world. You're at the polls index.")

#def posts_list(request):
#    posts = Post.published.all()
#    paginator = Paginator(posts, 2)
#    page_number = request.GET.get('page', 1)
#    try:
#        posts = paginator.page(page_number)
#    except PageNotAnInteger:
#        posts = paginator.page(1)
#    except EmptyPage:
#       posts = paginator.page(paginator.num_pages)
#    context = {
#        'posts': posts,
#    }
#    return render(request,'blog/list.html',context)

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = "blog/list.html"

def posts_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
   # try:
    #    post = Post.published.get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404("Post does not exist")
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request,"blog/detail.html",context)


'''
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    '''

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket(
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject'],
                message=cd['message'],
            )
            ticket_obj.save()

            return redirect("blog:index")

    else:
        form = TicketForm()
    return render(request, "forms/ticket.html",{'form':form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
            'post': post,
            'form': form,
            'comment': comment,
        }
    return render(request, "forms/comment.html", context)


def post_search(request):
    query = None
    results = []
    form = PostSearch(data=request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Post.published.annotate(similarity=Greatest(TrigramSimilarity('title', query),\
                                                              TrigramSimilarity('description', query),\
                                                              TrigramSimilarity('images__title', query)))\
        .filter(similarity__gt=0.1).order_by('-similarity').distinct()
    context = {"query" : query,
               "results" : results,
               }
    return render(request, "blog/search.html", context)



# simple search without postgres just django
#        results = Post.published.filter(title__icontains=query)

# multi search field with vector instead of Q object
#         results = Post.published.annotate(search=SearchVector('title','description')).\
#             filter(search=query).order_by('-search')

# advanced search with SearchQuery & rank and weight filtering
# in this code SearchVector is responsible for handling multi field search
#         search_query = SearchQuery(query)
#         search_vector = SearchVector('title', weight='B') + SearchVector('description', weight='A')
#         results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).\
#              filter(rank__gte=0.5).order_by('-rank')

# search without wieght filtering just ranking
#         search_query = SearchQuery(query)
#         search_vector = SearchVector('title', 'description')
#         results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).\
#               filter(search=search_query).order_by('-rank')


def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    return render(request, "blog/profile.html", {'posts':posts})