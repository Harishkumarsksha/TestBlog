from django.shortcuts import render, get_object_or_404

# Create your views here.

# implementation of the ListView and DetailView by FBV
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Blog.models import Post

# class based views for the pagination
from django.views.generic import ListView
from django.core.mail import send_mail
from Blog.forms import EmailSendForm, CommentForm
from Blog.models import Comment
from taggit.models import Tag


class PostListView(ListView):
    model = Post
    paginate_by = 1


def post_list_view(request, tag_slug=None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 4)

    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)

    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'Blog/post_list.html', {'post_list': post_list, 'tag': tag})


def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    comments = post.comment.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True

    else:
        form = CommentForm()
    return render(request, 'Blog/post_detail.html', {'post': post, 'form': form, 'comments': comments, 'csumit': csubmit})


def mail_send_view(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False
    form = EmailSendForm()
    if request.method == 'POST':
        form = EmailSendForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}{} recomend you tot read the {}'.format(
                cd['name'], cd['email'], post.title)

            message = 'Read Post At: \n{}\n\n{}\n comments :\n{}'.format(
                post_url, cd['name'], cd['comments'])
            send_mail(subject, message,
                      'harishkumarksha0@gmail.com', [cd['to']])
            sent = True
    return render(request, 'Blog/sharebymail.html', {'post': post, 'form': form, 'sent': sent})
