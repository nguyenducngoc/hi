# Django imports.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.generic import View

# Blog app imports.
from blog.forms.blog.article_forms import ArticleUpdateForm, ArticleCreateForm
from blog.models.article_models import Article


class DashboardHomeView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'dashboard/author/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        articles_list = Article.objects.filter(author=request.user)

        total_articles_written = len(articles_list)
        total_articles_published = len(
            articles_list.filter(status=Article.PUBLISHED, deleted=False))
        total_articles_views = sum(article.views for article in articles_list)
        total_articles_comments = sum(
            article.comments.count() for article in articles_list)

        recent_published_articles_list = articles_list.filter(
            status=Article.PUBLISHED, deleted=False).order_by("-date_published")[:5]

        self.context['total_articles_written'] = total_articles_written
        self.context['total_articles_published'] = total_articles_published
        self.context['total_articles_views'] = total_articles_views
        self.context['total_articles_comments'] = total_articles_comments
        self.context['recent_published_articles_list'] = recent_published_articles_list

        return render(request, self.template_name, self.context)


class ArticleWriteView(LoginRequiredMixin, View):

    SAVE_AS_DRAFT = "SAVE_AS_DRAFT"
    PUBLISH = "PUBLISH"

    template_name = 'dashboard/author/article_create_form.html'
    context_object = {}

    def get(self, request, *args, **kwargs):

        article_create_form = ArticleCreateForm()
        self.context_object["article_create_form"] = article_create_form

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        article_create_form = ArticleCreateForm(request.POST, request.FILES)

        action = request.POST.get("action")
        article_status = request.POST["status"]

        if action == self.SAVE_AS_DRAFT:

            if article_status == Article.PUBLISHED:
                self.context_object["article_create_form"] = article_create_form
                messages.error(request,
                               "B???n ???? l??u b??i vi???t d?????i d???ng b???n nh??p nh??ng "
                               "???? ch???n tr???ng th??i l?? '???? XU???T B???N'. B???n kh??ng "
                               "th??? l??u m???t b??i vi???t c?? tr???ng th??i '???? XU???T B???N' "
                               "d?????i d???ng b???n nh??p. Vui l??ng thay ?????i tr???ng th??i th??nh"
                               "'B???N TH???O' tr?????c b???n l??u b??i vi???t d?????i d???ng b???n nh??p.")
                return render(request, self.template_name, self.context_object)

            if article_create_form.is_valid():

                new_article = article_create_form.save(commit=False)
                new_article.author = request.user
                new_article.date_published = None
                new_article.save()
                article_create_form.save_m2m()

                messages.success(request, f"B??i vi???t ???????c so???n th???o th??nh c??ng.")
                return redirect("blog:drafted_articles")

            self.context_object["article_create_form"] = article_create_form
            messages.error(request, "Vui l??ng ??i???n ?????y ????? th??ng tin")
            return render(request, self.template_name, self.context_object)

        if action == self.PUBLISH:

            if article_status == Article.DRAFTED:
                self.context_object["article_create_form"] = article_create_form

                messages.error(request,
                               "B???n ???? nh???p v??o 'PUBLISH' ????? xu???t b???n b??i vi???t"
                               "nh??ng l???i ch???n tr???ng th??i l?? 'So???n th???o'"
                               "B???n kh??ng th??? Xu???t b???n m???t b??i vi???t c?? tr???ng th??i "
                               "l??'B???N TH???O'. Vui l??ng thay ?????i tr???ng th??i th??nh "
                               "'???? XU???T B???N' tr?????c khi b???n c?? th??? Xu???t b???n b??i vi???t ")
                return render(request, self.template_name, self.context_object)

            if article_create_form.is_valid():
                new_article = article_create_form.save(commit=False)
                new_article.author = request.user
                new_article.save()
                article_create_form.save_m2m()

                messages.success(self.request, f"B??i vi???t ???? ???????c xu???t b???n")
                return redirect(to="blog:dashboard_article_detail", slug=new_article.slug)

            self.context_object["article_create_form"] = article_create_form
            messages.error(request, "Vui l??ng ??i???n ?????y ????? th??ng tin")
            return render(request, self.template_name, self.context_object)


class ArticleUpdateView(LoginRequiredMixin, View):

    SAVE_AS_DRAFT = "SAVE_AS_DRAFT"
    PUBLISH = "PUBLISH"

    template_name = 'dashboard/author/article_update_form.html'
    context_object = {}

    def get(self, request, *args, **kwargs):

        old_article = get_object_or_404(Article, slug=self.kwargs.get("slug"))
        article_update_form = ArticleUpdateForm(instance=old_article, initial={'tags': old_article.tags.names})

        self.context_object["article_update_form"] = article_update_form
        self.context_object["article"] = old_article
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        old_article = get_object_or_404(Article, slug=self.kwargs.get("slug"))
        article_update_form = ArticleCreateForm(request.POST, request.FILES, instance=old_article)

        action = request.POST.get("action")
        article_status = request.POST["status"]

        if action == self.SAVE_AS_DRAFT:

            if article_status == Article.PUBLISHED:
                self.context_object["article_update_form"] = article_update_form
                messages.error(request,
                               "B???n ???? l??u b??i vi???t d?????i d???ng so???n th???o nh??ng  "
                               "???? ???????c ch???n tr???ng th??i l?? '???? XU???T B???N'. B???n "
                               "kh??ng th??? l??u b??i vi???t c?? tr???ng th??i '???? XU???T B???N'"
                               "d?????i d???ng b???n nh??p. Vui l??ng thay ?????i tr???ng th??i th??nh"
                               "'B???N TH???O' tr?????c b???n l??u b??i vi???t d?????i d???ng b???n nh??p.")
                return render(request, self.template_name, self.context_object)

            if not request.user == old_article.author.username:
                messages.error(request=self.request, message="B???n kh??ng c?? quy???n c???p nh???t b??i vi???t n??y.")
                return redirect(to="blog:written_articles")

            if article_update_form.is_valid():
                updated_article = article_update_form.save(commit=False)
                updated_article.author = request.user
                updated_article.date_published = None
                updated_article.date_updated = timezone.now()
                updated_article.save()
                article_update_form.save_m2m()

                messages.success(request, f"B??i vi???t ???? ???????c so???n th???o th??nh c??ng")
                return redirect("blog:drafted_articles")

            self.context_object["article_update_form"] = article_update_form
            messages.error(request, "Vui l??ng ??i???n ?????y ????? th??ng tin")
            return render(request, self.template_name, self.context_object)

        if action == self.PUBLISH:

            if article_status == Article.DRAFTED:
                self.context_object["article_update_form"] = article_update_form

                messages.error(request,
                               "B???n ???? nh???p v??o 'PUBLISH' ????? xu???t b???n b??i vi???t"
                               " nh??ng ???? ch???n tr???ng th??i l?? 'B???N TH???O'. "
                               "B???n kh??ng th??? xu???t b???n m???t b??i vi???t c?? tr???ng "
                               "th??i l?? 'D??? TH???O'. Vui l??ng thay ?????i tr???ng th??i "
                               "th??nh '???? XU???T B???N' tr?????c khi b???n c?? th??? Xu???t b???n "
                               "b??i vi???t.")
                return render(request, self.template_name, self.context_object)

            if article_update_form.is_valid():

                updated_article = article_update_form.save(commit=False)
                updated_article.author = request.user
                updated_article.date_published = timezone.now()
                updated_article.date_updated = timezone.now()
                updated_article.save()
                article_update_form.save_m2m()

                messages.success(self.request, f"B??i vi???t ???? ???????c c???p nh???t.")
                return redirect(to="blog:dashboard_article_detail", slug=updated_article.slug)

            self.context_object["article_update_form"] = article_update_form
            messages.error(request, "Vui l??ng ??i???n ?????y ????? th??ng tin")
            return render(request, self.template_name, self.context_object)


class ArticleDeleteView(LoginRequiredMixin, View):
    """
      Deletes article
    """

    def get(self, *args, **kwargs):
        """
           Checks if user who has requested to delete the article is the
           owner of the article.
           If the user is the owner, it sets the deleted field of the article to true and
           return a successful message.
           If the user is not the owner, it tells user he/she can't delete it
        """
        article = get_object_or_404(Article, slug=self.kwargs.get("slug"))

        if not self.request.user.username == article.author.username:
            messages.error(request=self.request, message="B???n kh??ng c?? quy???n x??a b??i vi???t n??y.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

        article.deleted = True
        article.save()

        messages.success(request=self.request, message="???? x??a b??i vi???t")
        return redirect(to='blog:deleted_articles')


class DashboardArticleDetailView(LoginRequiredMixin, View):
    """
       Displays article details.
    """

    def get(self, request, *args, **kwargs):
        """
           Returns article details.
        """
        template_name = 'dashboard/author/dashboard_article_detail.html'
        context_object = {}

        article = get_object_or_404(Article, slug=self.kwargs.get("slug"))

        context_object['article_title'] = article.title
        context_object['article'] = article

        return render(request, template_name, context_object)


class ArticlePublishView(LoginRequiredMixin, View):
    """
       View to publish a drafted article
    """

    def get(self, request, *args, **kwargs):
        """
            Gets article slug from user and gets the article from the
            database.
            It then sets the status to publish and date published to now and
            then save the article and redirects the author to his/her published
            articles.
        """
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        article.status = Article.PUBLISHED
        article.date_published = timezone.now()
        article.date_updated = timezone.now()
        article.save()

        messages.success(request, f"???? xu???t b???n b??i vi???t th??nh c??ng.")
        return redirect('blog:dashboard_article_detail', slug=article.slug)


class AuthorWrittenArticlesView(LoginRequiredMixin, View):
    """
       Displays all articles written by an author.
    """

    def get(self, request):
        """
           Returns all articles written by an author.
        """
        template_name = 'dashboard/author/author_written_article_list.html'
        context_object = {}

        written_articles = Article.objects.filter(author=request.user.id, deleted=False).order_by('-date_created')
        total_articles_written = len(written_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(written_articles, 5)
        try:
            written_articles_list = paginator.page(page)
        except PageNotAnInteger:
            written_articles_list = paginator.page(1)
        except EmptyPage:
            written_articles_list = paginator.page(paginator.num_pages)

        context_object['written_articles_list'] = written_articles_list
        context_object['total_articles_written'] = total_articles_written

        return render(request, template_name, context_object)


class AuthorPublishedArticlesView(LoginRequiredMixin, View):
    """
       Displays published articles by an author.
    """

    def get(self, request):
        """
           Returns published articles by an author.
        """
        template_name = 'dashboard/author/author_published_article_list.html'
        context_object = {}

        published_articles = Article.objects.filter(author=request.user.id,
                                                    status=Article.PUBLISHED, deleted=False).order_by('-date_published')
        total_articles_published = len(published_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(published_articles, 5)
        try:
            published_articles_list = paginator.page(page)
        except PageNotAnInteger:
            published_articles_list = paginator.page(1)
        except EmptyPage:
            published_articles_list = paginator.page(paginator.num_pages)

        context_object['published_articles_list'] = published_articles_list
        context_object['total_articles_published'] = total_articles_published

        return render(request, template_name, context_object)


class AuthorDraftedArticlesView(LoginRequiredMixin, View):
    """
       Displays drafted articles by an author.
    """

    def get(self, request):
        """
           Returns drafted articles by an author.
        """
        template_name = 'dashboard/author/author_drafted_article_list.html'
        context_object = {}

        drafted_articles = Article.objects.filter(author=request.user.id,
                                                  status=Article.DRAFTED, deleted=False).order_by('-date_created')
        total_articles_drafted = len(drafted_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(drafted_articles, 5)
        try:
            drafted_articles_list = paginator.page(page)
        except PageNotAnInteger:
            drafted_articles_list = paginator.page(1)
        except EmptyPage:
            drafted_articles_list = paginator.page(paginator.num_pages)

        context_object['drafted_articles_list'] = drafted_articles_list
        context_object['total_articles_drafted'] = total_articles_drafted

        return render(request, template_name, context_object)


class AuthorDeletedArticlesView(LoginRequiredMixin, View):
    """
       Displays deleted articles by an author.
    """

    def get(self, request):
        """
           Returns deleted articles by an author.
        """
        template_name = 'dashboard/author/author_deleted_article_list.html'
        context_object = {}

        deleted_articles = Article.objects.filter(author=request.user.id,
                                                  deleted=True).order_by('-date_published')
        total_articles_deleted = len(deleted_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(deleted_articles, 5)
        try:
            deleted_articles_list = paginator.page(page)
        except PageNotAnInteger:
            deleted_articles_list = paginator.page(1)
        except EmptyPage:
            deleted_articles_list = paginator.page(paginator.num_pages)

        context_object['deleted_articles_list'] = deleted_articles_list
        context_object['total_articles_deleted'] = total_articles_deleted

        return render(request, template_name, context_object)
