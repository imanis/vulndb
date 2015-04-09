from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from vulnDB.vulns.models import Vuln, VulnCategory, VulnItem, VulnSeverityMatrix, VulnActionPriorityMatrix, VulnType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from vulnDB.vulns.forms import VulnForm, VulnCategoryForm
from vulnDB.feeds.models import Feed
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from vulnDB.decorators import ajax_required
import markdown
import json
from django.template.loader import render_to_string
from eztables.views import DatatablesView


def _vulns(request, vulns):
    '''
    paginator = Paginator(vulns, 10)
    page = request.GET.get('page')
    try:
        vulns = paginator.page(page)
    except PageNotAnInteger:
        vulns = paginator.page(1)
    except EmptyPage:
        vulns = paginator.page(paginator.num_pages)
    '''

    # vulns = Vuln.get_published()
    popular_categories = VulnCategory.get_popular_categories()
    popular_types = VulnType.get_popular_types()

    return render(request, 'vulns/vulns.html',
                  {'vulns': vulns, 'popular_categories': popular_categories, 'popular_types': popular_types})


@login_required
def vulns(request):
    all_vulns = Vuln.get_published()
    return _vulns(request, all_vulns)


@login_required
def vuln(request, slug):
    vuln = get_object_or_404(Vuln, slug=slug, status=Vuln.PUBLISHED)
    return render(request, 'vulns/vuln.html', {'vuln': vuln})


@login_required
def category(request, cat_name):
    vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
    vulns_a = []
    for v in vulns:
        if v.category.category == cat_name:
            vulns_a.append(v)
    return _vulns(request, vulns_a)


@login_required
def type(request, type_name):
    vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
    vulns_a = []
    for v in vulns:
        if v.type.type == type_name:
            vulns_a.append(v)
    return _vulns(request, vulns_a)


@login_required
def add(request):
    if request.method == 'POST':
        form = VulnForm(request.POST)
        if form.is_valid():
            vuln = Vuln()
            vuln.create_user = request.user
            vuln.ref = form.cleaned_data.get('ref')
            vuln.vulnerability = form.cleaned_data.get('vulnerability')
            vuln.description = form.cleaned_data.get('description')
            vuln.recommendation = form.cleaned_data.get('recommendation')
            # vuln.severity = form.cleaned_data.get('severity')
            vuln.type = form.cleaned_data.get('type')
            vuln.nature = form.cleaned_data.get('nature')
            vuln.category = form.cleaned_data.get('category')
            vuln.exploitation_impact = form.cleaned_data.get('exploitation_impact')
            vuln.exploitation_complexity = form.cleaned_data.get('exploitation_complexity')
            vuln.action_complexity = form.cleaned_data.get('action_complexity')
            vuln.action_priority = form.cleaned_data.get('action_priority')

            status = form.cleaned_data.get('status')
            if status in [Vuln.PUBLISHED, Vuln.DRAFT]:
                vuln.status = form.cleaned_data.get('status')

            vuln.severity = VulnSeverityMatrix.get_rule(vuln.exploitation_complexity, vuln.exploitation_impact)
            vuln.action_priority = VulnActionPriorityMatrix.get_rule(vuln.action_complexity, vuln.severity)

            vuln.save()
            Adding_vuln_post = u'{0} Add a new Vulnerability <a href="/vulns/{1}/">{2}</a> to the Database.'.format(
                request.user, vuln.slug, vuln.vulnerability)
            feed = Feed(user=request.user, post=Adding_vuln_post)
            feed.save()
            request.user.profile.notify_Adding_vuln(vuln)

            affected_item_tags = form.cleaned_data.get('affected_item_tags')
            vuln.create_items_tags(affected_item_tags)
            return redirect('/vulns/')
    else:
        form = VulnForm()
    form1 = VulnCategoryForm()
    return render(request, 'vulns/add.html', {'form': form, 'form1': form1})


@login_required
def drafts(request):
    drafts = Vuln.objects.filter(create_user=request.user, status=Vuln.DRAFT)
    return render(request, 'vulns/drafts.html', {'drafts': drafts})


@login_required
def preferences(request):
    return render(request, 'vulns/preferences.html')


@login_required
def edit(request, id):
    if id:
        vuln = get_object_or_404(Vuln, pk=id)
        vuln.update_user = request.user
    else:
        vuln = Vuln(create_user=request.user)

    if request.POST:
        form = VulnForm(request.POST, instance=vuln)
        tags=[]
        if form.is_valid():
            print >> form.vulnerability
            form.save()
            affected_item_tags = form.cleaned_data.get('affected_item_tags')
            vuln.create_items_tags(affected_item_tags)
            vuln.status= form.cleaned_data.get('status')
            return redirect('/vulns/')
    else:
        form = VulnForm(instance=vuln)
        tags = [tag.tag for tag in vuln.get_items_tags()]

    return render(request, 'vulns/edit.html', {'form': form, 'tags': tags})


@login_required
def delete(request, id):
    if id:
        vuln = get_object_or_404(Vuln, pk=id)
        if vuln.create_user == request.user:
            vuln.delete()
    return redirect('/vulns/')


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('description')
            html = 'Nothing to display :('
            if len(content.strip()) > 0:
                html = content
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()


'''
@login_required
@ajax_required
def comment(request):
    try:
        if request.method == 'POST':
            vuln_id = request.POST.get('vuln')
            vuln = Vuln.objects.get(pk=vuln_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                vuln_comment = VulnComment(user=request.user, vuln=vuln, comment=comment)
                vuln_comment.save()
            html = u''
            for comment in vuln.get_comments():
                html = u'{0}{1}'.format(html, render_to_string('vulns/partial_vuln_comment.html', {'comment': comment}))
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()

'''


@login_required
def item_tag(request, tag_name):
    tags = VulnItem.objects.filter(tag=tag_name)
    vulns = []
    for tag in tags:
        if tag.vuln.status == Vuln.PUBLISHED:
            vulns.append(tag.vuln)
    return _vulns(request, vulns)


@login_required
def delete_item_tag(request, tag_name, vuln_id):
    vuln = get_object_or_404(Vuln, pk=vuln_id)

    tag = VulnItem.objects.filter(tag=tag_name, vuln=vuln).first()
    tag.delete()

    form = VulnForm(instance=vuln)
    tags = [tag.tag for tag in vuln.get_items_tags()]
    return render(request, 'vulns/edit.html', {'form': form, 'tags': tags})


@login_required
@ajax_required
def categories(request):
    categories = VulnCategory.objects.filter()
    dump = []
    template = u'{0} ({1})'
    for cat in categories:
        dump.append(cat.catergory)
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


@login_required
def add_category(request):
    data = {}
    if request.method == 'POST':
        form = VulnCategoryForm(request.POST)
        if form.is_valid():
            vulnCategory = VulnCategory()
            vulnCategory.category = form.cleaned_data.get('category')
            vulnCategory.save()
            data['new_item_value'] = vulnCategory.category;
            data['new_item_key'] = vulnCategory.pk;
            data['stat'] = "ok";
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error";
            return render(request, 'vulns/add_category_modal.html', {'form': form})
    else:
        form = VulnCategoryForm()
        return render(request, 'vulns/add_category_modal.html', {'form': form})
