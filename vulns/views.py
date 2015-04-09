from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from vulnDB.vulns.models import Vuln, VulnCategory, VulnSeverityMatrix, VulnActionPriorityMatrix, VulnType, Tag, \
    VulnExploitation_complexity \
    , VulnExploitation_impact, VulnSeverity, VulnAction_complexity, VulnAction_priority
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from vulnDB.vulns.forms import *
from vulnDB.feeds.models import Feed
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from vulnDB.decorators import ajax_required
import markdown
import json
from django.template.loader import render_to_string
from eztables.views import DatatablesView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from vulnDB.projects.models import ProjectNature
from django.utils.translation import ugettext as _


# Representation Methods

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
    popular_natures = ProjectNature.get_popular_nature()

    return render(request, 'vulns/vulns.html',
                  {'vulns': vulns, 'popular_categories': popular_categories, 'popular_types': popular_types,
                   'popular_natures': popular_natures})

@login_required
def vulns(request):
    all_vulns = Vuln.get_published()
    return _vulns(request, all_vulns)

@login_required
def drafts(request):
    drafts = Vuln.objects.filter(create_user=request.user, status=Vuln.DRAFT)
    return render(request, 'vulns/drafts.html', {'drafts': drafts})

@login_required
def vuln(request, slug):
    vuln = get_object_or_404(Vuln, slug=slug, status=Vuln.PUBLISHED)
    return render(request, 'vulns/vuln.html', {'vuln': vuln})

@login_required
def index_category(request, cat_name):
    vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
    vulns_a = []
    for v in vulns:
        if v.category.category == cat_name:
            vulns_a.append(v)
    return _vulns(request, vulns_a)

@login_required
def index_type(request, type_name):
    vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
    vulns_a = []
    for v in vulns:
        if v.type.type == type_name:
            vulns_a.append(v)
    return _vulns(request, vulns_a)

@login_required
def index_nature(request, nature_name):
    vulns = Vuln.objects.filter(status=Vuln.PUBLISHED)
    vulns_a = []
    for v in vulns:
        if v.nature.nature == nature_name:
            vulns_a.append(v)
    return _vulns(request, vulns_a)


# CRUD Methods for Vuln

@login_required
@permission_required('Vulns.add_vuln')
def add(request):
    if request.method == 'POST':
        form = VulnForm(request.POST)
        if form.is_valid():
            vuln = Vuln()
            vuln.create_user = request.users
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

            # add tags
            tags = form.cleaned_data.get('tags')
            vuln.create_tags(tags)

            adding_vuln_post = ''.join([ u'<span class="glyphicon glyphicon-pencil"></span> ',
                                         _("Add a new Vulnerability"),
                                       u' <a href="/vulns/{0}/">{1}</a> '.format(vuln.slug, vuln.vulnerability),
                                       _(" to the Database.")])
            feed = Feed(user=request.user, post=adding_vuln_post)
            feed.save()
            request.user.profile.notify_Adding_vuln(vuln)
            return redirect('/vulns/')

        tagsliste = [tag[1:-1] for tag in request.POST['tags'][1:-1].split(",")]

    else:
        tagsliste = []
        form = VulnForm()
    form1 = VulnCategoryForm()
    tags = [i.name for i in Tag.objects.all()]
    return render(request, 'vulns/add.html', {'tags': tags, 'form': form, 'form1': form1, 'tagsliste': tagsliste})

@login_required
@permission_required('Vulns.change_vuln')
def edit(request, id):
    if id:
        vuln = get_object_or_404(Vuln, pk=id)
        vuln.update_user = request.user
    else:
        vuln = Vuln(create_user=request.user)

    if request.POST:
        form = VulnForm(request.POST, instance=vuln)
        if form.is_valid():
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


            # add tags
            vuln.tags.through.objects.filter(vuln__id=vuln.id).delete()
            tags = form.cleaned_data.get('tags')
            vuln.create_tags(tags)
            vuln.save()
            edit_vuln_post = ''.join([ u' <span class="glyphicon glyphicon-refresh"></span> ',
                                         _("Modify a Vulnerability"),
                                       u' <a href="/vulns/{0}/">{1}</a> '.format(vuln.slug, vuln.vulnerability)])
            feed = Feed(user=request.user, post=edit_vuln_post)
            feed.save()
            if vuln.status == Vuln.PUBLISHED:
                return redirect('/vulns/' + vuln.slug)
            else:
                return redirect('/vulns/drafts')
        tagsliste = [tag[1:-1] for tag in request.POST['tags'][1:-1].split(",")]
    else:
        form = VulnForm(instance=vuln)
        tagsliste = vuln.get_items_tags()
        tags = [i.name for i in Tag.objects.all()]
        return render(request, 'vulns/edit.html', {'tagsliste': tagsliste, 'tags': tags, 'form': form})

    tags = [i.name for i in Tag.objects.all()]
    return render(request, 'vulns/edit.html', {'tagsliste': tagsliste, 'tags': tags, 'form': form})

@login_required
@permission_required('Vulns.delete_vuln')
def delete(request, id):
    if id:
        vuln = get_object_or_404(Vuln, pk=id)
        if vuln.create_user == request.user:
            delete_vuln_post = ''.join([ u' <span class="glyphicon glyphicon-trash"></span> ',
                                         _("Delete a Vulnerability"),
                                       u' <b>{0}</b> '.format(vuln.vulnerability),
                                       _("From the Database")])
            feed = Feed(user=request.user, post=delete_vuln_post)
            feed.save()

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


# CRUD for item Tag

@login_required
def item_tag(request, tag_name):
    tag = Tag.objects.filter(name=tag_name).first()
    vulns = []
    for vuln in tag.vuln_set.all():
        if vuln.status == Vuln.PUBLISHED:
            vulns.append(vuln)
    return _vulns(request, vulns)


# CRUD Methods for CVSS

@login_required
def preferences(request, etat):
    exploitation_complexity = VulnExploitation_complexity.objects.all()
    exploitation_impact = VulnExploitation_impact.objects.all()
    action_complexity = VulnAction_complexity.objects.all()
    action_priority = VulnAction_priority.objects.all().exclude(action_priority="Empty")
    severity = VulnSeverity.objects.all().exclude(severity="Empty")

    formServity = ChangeServityForm()
    formAction = ChangeActionForm()
    return render(request, 'vulns/preferences.html', {'etat': etat, 'exploitation_impact': exploitation_impact,
                                                      'exploitation_complexity': exploitation_complexity, \
                                                      'action_complexity': action_complexity,
                                                      'severity_liste': severity, 'formServity': formServity,
                                                      'formAction': formAction, 'action_priority': action_priority})

@login_required
@permission_required('Vulns.change_vulnseveritymatrix')
def change_serevity(request, serevety_id):
    if request.method == 'POST':
        form = ChangeServityForm(request.POST)
        if form.is_valid():
            severity_matrix = VulnSeverityMatrix.objects.get(id=serevety_id)
            severity_matrix.severity = VulnSeverity.objects.get(id=form.cleaned_data['severity'].id)
            severity_matrix.save()
            update_serevity = ''.join([ u' <span class="glyphicon glyphicon-th"></span> ',
                                         _("Update Globale Servety Matrix")])
            feed = Feed(user=request.user, post=update_serevity)
            feed.save()
            return redirect('preferences', etat='severity')
    return redirect('preferences', etat='severity')

@login_required
@permission_required('Vulns.change_vulnactionprioritymatrix')
def change_action(request, action_id):
    if request.method == 'POST':
        form = ChangeActionForm(request.POST)
        if form.is_valid():
            actino_matrix = VulnActionPriorityMatrix.objects.get(id=action_id)
            actino_matrix.action_priority = VulnAction_priority.objects.get(id=form.cleaned_data['action'].id)
            actino_matrix.save()
            update_action = ''.join([ u' <span class="glyphicon glyphicon-th"></span> ',
                                         _("Update Globale Action Priority Matrix")])
            feed = Feed(user=request.user, post=update_action)
            feed.save()
            return redirect('preferences', etat='priority')
    return redirect('preferences', etat='priority')



@login_required
@permission_required('Vulns.add_vulnseverity')
def action_add(request, action):
    etat = 'severity'
    if action == 'exploitation_impact':
        form = ExploitationImpactForm(request.POST or None)
    elif action == 'action_complexity':
        form = ActionComplexityForm(request.POST or None)
        etat = 'priority'
    elif action == 'exploitation_complexity':
        form = ExploitationComplexityForm(request.POST or None)
    elif action == 'action_priority':
        form = ActionPriorityForm(request.POST or None)
        etat = 'priority'
    elif action == 'severity':
        form = SeverityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('preferences', etat=etat)
    return render(request, 'vulns/matrix/add_action.html', {'action': action, 'form': form})


@login_required
@permission_required('Vulns.change_vulnseverity')
def action_edit(request, id, action):
    etat = 'severity'
    if action == 'exploitation_impact':
        instance = VulnExploitation_impact.objects.get(id=id)
        form = ExploitationImpactForm(request.POST or None, instance=instance)
    elif action == 'action_complexity':
        instance = VulnAction_complexity.objects.get(id=id)
        form = ActionComplexityForm(request.POST or None, instance=instance)
        etat = 'priority'
    elif action == 'exploitation_complexity':
        instance = VulnExploitation_complexity.objects.get(id=id)
        form = ExploitationComplexityForm(request.POST or None, instance=instance)
    elif action == 'action_priority':
        instance = VulnAction_priority.objects.get(id=id)
        form = ActionPriorityForm(request.POST or None, instance=instance)
        etat = 'priority'
    elif action == 'severity':
        instance = VulnSeverity.objects.get(id=id)
        form = SeverityForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('preferences', etat=etat)
    return render(request, 'vulns/matrix/edit_action.html', {'action': action, 'form': form})


@login_required
@permission_required('Vulns.delete_vulnseverity')
def action_delete(request, id, action):
    etat = 'severity'
    if action == 'exploitation_impact':
        exploitation_impact = VulnExploitation_impact.objects.get(id=id)
        exploitation_impact.delete()
    elif action == 'action_complexity':
        action_complexity = VulnAction_complexity.objects.get(id=id)
        action_complexity.delete()
        etat = 'priority'
    elif action == 'exploitation_complexity':
        exploitation_complexity = VulnExploitation_complexity.objects.get(id=id)
        exploitation_complexity.delete()
    elif action == 'action_priority':
        action_priority = VulnAction_priority.objects.get(id=id)
        action_priority.delete()
        etat = 'priority'
    elif action == 'severity':
        severity = VulnSeverity.objects.get(id=id)
        severity.delete()

    return redirect('preferences', etat=etat)


'''
@login_required
def add_category(request):
    data = {}
    if request.method == 'POST':
        form = VulnCategoryForm(request.POST)
        if form.is_valid():
            vulnCategory = VulnCategory()
            vulnCategory.category = form.cleaned_data.get('category')
            vulnCategory.save()
            adding_category_post = u' <span class="glyphicon glyphicon-pencil"></span> {0} Add a new Vulnerabilities Category {1} .'.format(
                request.user, vuln.vulnCategory)
            feed = Feed(user=request.user, post=adding_category_post)
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

'''

