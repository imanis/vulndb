from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, _get_queryset
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.utils.unittest.main import CATCHBREAK
from vulnDB.projects.forms import *
from vulnDB.projects.models import *
from vulnDB.vulns.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from vulnDB.vulns.forms import VulnForm, VulnCategoryForm
from vulnDB.feeds.models import Feed
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .chart import ChartData
from vulnDB.decorators import ajax_required
import markdown
import json
from django.template.loader import render_to_string
from eztables.views import DatatablesView
from django.shortcuts import redirect
from django.conf import settings as django_settings
import os
from PIL import Image
from django.utils.translation import ugettext as _


@login_required
def _projects(request, projects, active):
    paginator = Paginator(projects, 10)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'projects/projects.html', {'projects': projects, 'active': active})


@login_required
def projects(request):
    return active(request)


@login_required
def active(request):
    projects = Project.get_active()
    return _projects(request, projects, 'active')


@login_required
def archived(request):
    projects = Project.get_archived()
    return _projects(request, projects, 'archived')


@login_required
def all(request):
    projects = Project.objects.all()
    return _projects(request, projects, 'all')


@login_required
def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    request.session['active_project'] = project.pk
    request.session['active_project_slug'] = slug
    vulns = VulnInst.objects.filter(project=project)
    return render(request, 'projects/project.html', {'project': project, 'vulns': vulns})


@login_required
@permission_required('Projects.add_project')
def start(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.create_user = request.user
            project.project = form.cleaned_data.get('project')
            project.nature = form.cleaned_data.get('nature')
            project.client = form.cleaned_data.get('client')
            project.status = Project.ACTIVE
            project.teammanager = request.user
            project.save()

            # add all cssv global to project instance
            for i in VulnExploitation_impact.objects.all():
                c = ProjectExploitation_impact(exploitation_impact=i.exploitation_impact, project=project,
                                               color=i.color)
                c.save()

            for i in VulnExploitation_complexity.objects.all():
                c = ProjectExploitation_complexity(exploitation_complexity=i.exploitation_complexity, project=project,
                                                   color=i.color)
                c.save()

            for i in VulnAction_complexity.objects.all():
                c = ProjectAction_complexity(action_complexity=i.action_complexity, project=project, color=i.color)
                c.save()

            for i in VulnSeverity.objects.all():
                c = ProjectSeverity(severity=i.severity, project=project, color=i.color)
                c.save()

            for i in VulnAction_priority.objects.all():
                c = ProjectAction_priority(action_priority=i.action_priority, project=project, color=i.color)
                c.save()

            for i in VulnSeverityMatrix.objects.all():
                exploitation_impact = ProjectExploitation_impact.objects.get(
                    exploitation_impact=i.exploitation_impact.exploitation_impact, project__id=project.id)
                exploitation_complexity = ProjectExploitation_complexity.objects.get(
                    exploitation_complexity=i.exploitation_complexity.exploitation_complexity, project__id=project.id)
                severity = ProjectSeverity.objects.get(severity=i.severity.severity, project__id=project.id)
                c = ProjectSeverityMatrix(exploitation_impact=exploitation_impact,
                                          exploitation_complexity=exploitation_complexity, severity=severity)
                c.save()

            for i in VulnActionPriorityMatrix.objects.all():
                action_complexity = ProjectAction_complexity.objects.get(
                    action_complexity=i.action_complexity.action_complexity, project__id=project.id)
                action_priority = ProjectAction_priority.objects.get(action_priority=i.action_priority.action_priority,
                                                                     project__id=project.id)
                severity = ProjectSeverity.objects.get(severity=i.severity.severity, project__id=project.id)
                c = ProjectActionPriorityMatrix(action_complexity=action_complexity, action_priority=action_priority,
                                                severity=severity)
                c.save()

           # add_project_post = u'<span class="glyphicon glyphicon-expand"></span> {0} '.format(request.user) + _(
            #    'Start a new Project') + u' <a href="/projects/{0}>{1}</a>.'.format(project.slug, project.project)


            add_project_post = ''.join([ u'<span class="glyphicon glyphicon-expand"> </span> ',
                                        _("has Start a new Project"),
                                        u' <a href="/projects/{1}">{0} </a>.'.format(project.project, project.slug) ])

            feed = Feed(user=request.user, post=add_project_post)
            feed.save()
            # request.user.profile.notify_Adding_vuln(project)

            return redirect('/projects/')
    else:
        form = ProjectForm()
    return render(request, 'projects/start.html', {'form': form})


@permission_required('Projects.change_project')
@login_required
def modify(request, id):
    if id:
        project = get_object_or_404(Project, pk=id)
        project.update_user = request.user
    else:
        project = Project(create_user=request.user)

    if request.POST:
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            modify_project_post = ''.join([ u'<span class="glyphicon glyphicon-refresh"> </span> ',
                                        _("Modify an existing Project"),
                                        u' <a href="/projects/{1}">{0} </a>.'.format(project.project, project.slug) ])
            feed = Feed(user=request.user, post=modify_project_post)
            feed.save()
            return redirect('/projects/' + project.slug)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/modify.html', {'form': form, 'projectid': project.pk})


@login_required
def remove(request, id):
    if id:
        project = get_object_or_404(Project, pk=id)
        if project.create_user == request.user:
            remove_project_post = ''.join([u'<span class="glyphicon glyphicon-trash"></span> ',
                                           _("Remove a Project"),
                                            u' <b> {1}</b> .'.format(request.user, project.project)])
            feed = Feed(user=request.user, post=remove_project_post)
            feed.save()
            project.delete()

    return redirect('/projects/')


@login_required
def archive(request, id):
    if id:
        project = get_object_or_404(Project, pk=id)
        if project.create_user == request.user:
            project.status = Project.ARCHIVED
            project.save()
            archive_project_post = ''.join([u'<span class="glyphicon glyphicon-file"></span> ',
                                           _("Archive an active Project"),
                                            u' <b> {1}</b> .'.format(request.user, project.project)])
            feed = Feed(user=request.user, post=archive_project_post)
            feed.save()
            return redirect('/projects/' + project.slug)
    return redirect('/projects/')


@login_required
def activate(request, id):
    if id:
        project = get_object_or_404(Project, pk=id)
        if project.create_user == request.user:
            project.status = Project.ACTIVE
            project.save()
            active_project_post = ''.join([u'<span class="glyphicon glyphicon-ok"></span> ',
                                           _("Activate an archived Project "),
                                            u' <b> {1}</b> .'.format(request.user, project.project)])
            feed = Feed(user=request.user, post=active_project_post)
            feed.save()
            return redirect('/projects/' + project.slug)
    return redirect('/projects/')


# project cssv
@login_required
def preferences(request, project_id, etat):
    exploitation_complexity = ProjectExploitation_complexity.objects.filter(project__id=project_id)
    exploitation_impact = ProjectExploitation_impact.objects.filter(project__id=project_id)
    action_complexity = ProjectAction_complexity.objects.filter(project__id=project_id)
    severity = ProjectSeverity.objects.filter(project__id=project_id).exclude(severity="Empty")
    action_priority = ProjectAction_priority.objects.all().exclude(action_priority="Empty")

    formServity = ChangeServityForm(project=project_id)
    formAction = ChangeActionForm(project=project_id)
    active_project_slug = request.session.get('active_project_slug', False)

    return render(request, 'projects/preferences.html',
                  {'action_priority': action_priority, 'project_id': project_id, 'active_project_slug' \
                      : active_project_slug, 'etat': etat, 'exploitation_impact': exploitation_impact,
                   'exploitation_complexity': exploitation_complexity, \
                   'action_complexity': action_complexity, 'severity_liste': severity, 'formServity': formServity,
                   'formAction': formAction})


# project cssv
@login_required
def project_change_serevity(request, serevety_id, project_id):
    if request.method == 'POST':
        form = ChangeServityForm(request.POST, project=project_id)
        if form.is_valid():
            severity_matrix = ProjectSeverityMatrix.objects.get(id=serevety_id)
            severity_matrix.severity = ProjectSeverity.objects.get(id=form.cleaned_data['severity'].id)
            severity_matrix.save()
            project = get_object_or_404(Project, pk=project_id)
            update_serevity = ''.join([ u'<span class="glyphicon glyphicon-th"> </span> ',
                                        _("Update Servety Matrix for the Project"),
                                        u' <a href="/projects/{1}">{0} </a>.'.format(project.project, project.slug) ])
            feed = Feed(user=request.user, post=update_serevity)
            feed.save()

            return redirect('preferences_project', etat='severity', project_id=project_id)


# project cssv
@login_required
def project_change_action(request, action_id, project_id):
    if request.method == 'POST':
        form = ChangeActionForm(request.POST, project=project_id)
        if form.is_valid():
            actino_matrix = ProjectActionPriorityMatrix.objects.get(id=action_id)
            actino_matrix.action_priority = ProjectAction_priority.objects.get(id=form.cleaned_data['action'].id)
            actino_matrix.save()

            project = get_object_or_404(Project, pk=project_id)
            update_action = ''.join([ u'<span class="glyphicon glyphicon-th"> </span> ',
                                        _("Update Action Priority Matrix for the Project"),
                                        u' <a href="/projects/{1}">{0} </a>.'.format(project.project, project.slug) ])

            feed = Feed(user=request.user, post=update_action)
            feed.save()
            return redirect('preferences_project', etat='priority', project_id=project_id)


# # Project Vulns Managment


@login_required
def load(request):
    queryset = _get_queryset(Vuln)
    errorMsg = ""
    active_project = request.session.get('active_project', False)
    if not active_project:
        return redirect('/projects/')
    else:
        if request.method == 'POST':
            form = VulnSelectionForm(request.POST)
            project = get_object_or_404(Project, pk=active_project)
            if form.is_valid():
                try:
                    ids = form.cleaned_data.get('ids').split(',')
                    for id_v in ids:

                        vref = float(id_v)
                        vuln = queryset.get(pk=id_v)
                        vulninst = VulnInst()
                        vulninst.base_pk = vref
                        vulninst.instanciate(vuln)
                        vulninst.project = project
                        vulninst.exploitation_impact = ProjectExploitation_impact.objects.get(project_id=project.id,
                                                                                              exploitation_impact=vuln.exploitation_impact.exploitation_impact)
                        vulninst.exploitation_complexity = ProjectExploitation_complexity.objects.get(
                            project_id=project.id,
                            exploitation_complexity=vuln.exploitation_complexity.exploitation_complexity)
                        vulninst.action_complexity = ProjectAction_complexity.objects.get(project_id=project.id,
                                                                                          action_complexity=vuln.action_complexity.action_complexity)
                        vulninst.save()
                        for tag in vuln.tags.all():
                            vulninst.tagsproject.add(tag)

                        vulninst.save()
                        vulninst = VulnInst.objects.filter(pk=vulninst.pk).first()
                        loding_vuln_post = ''.join([ u'<span class="glyphicon glyphicon-fire"> </span> ',
                                        _("Load a new Vulnerability"),
                                        u' <a href="/projects/show/{0}/">{1}</a>'.format( vulninst.pk, vulninst.vulnerability),
                                        _("to Project"),
                                        u' <a href="/projects/{0}/">{1}</a> .'.format(project.slug, project.project)])
                        feed = Feed(user=request.user, post=loding_vuln_post)
                        feed.save()
                        request.user.profile.notify_Adding_vulnInst(vulninst, project)
                except (ValueError, Exception, queryset.model.DoesNotExist):
                    errorMsg = _("You have entred a worng Refs / IDs")
            else:
                if form.data.__contains__('vref'):
                    vref = form.data.get('vref')
                    try:
                        vref = float(vref)
                        vuln = queryset.get(pk=vref)
                        vulninst = VulnInst()
                        vulninst.base_pk = vref
                        vulninst.instanciate(vuln)
                        vulninst.project = project
                        vulninst.exploitation_impact = ProjectExploitation_impact.objects.get(project_id=project.id,
                                                                                              exploitation_impact=vuln.exploitation_impact.exploitation_impact)
                        vulninst.exploitation_complexity = ProjectExploitation_complexity.objects.get(
                            project_id=project.id,
                            exploitation_complexity=vuln.exploitation_complexity.exploitation_complexity)
                        vulninst.action_complexity = ProjectAction_complexity.objects.get(project_id=project.id,
                                                                                          action_complexity=vuln.action_complexity.action_complexity)
                        vulninst.save()
                        for tag in vuln.tags.all():
                            vulninst.tagsproject.add(tag)
                        vulninst.save()
                        vulninst = VulnInst.objects.filter(pk=vulninst.pk).first()
                        loding_vuln_post = ''.join([ u'<span class="glyphicon glyphicon-fire"> </span> ',
                                        _("Load a new Vulnerability"),
                                        u' <a href="/projects/show/{0}/">{1}</a>'.format( vulninst.pk, vulninst.vulnerability),
                                        _("to Project"),
                                        u' <a href="/projects/{0}/">{1}</a> .'.format(project.slug, project.project)])
                        feed = Feed(user=request.user, post=loding_vuln_post)
                        feed.save()
                        request.user.profile.notify_Adding_vulnInst(vulninst, project)
                    except (ValueError, queryset.model.DoesNotExist):
                        errorMsg = _("You have entred a worng Ref / ID")

            if not errorMsg:
                if project:
                    return redirect('/projects/' + project.slug)
                else:
                    return redirect('/projects')

        project = active_project
        all_vulns = Vuln.get_published()
        form = VulnSelectionForm()
        return render(request, 'projects/vulns_selection.html',
                      {'vulns': all_vulns, 'project': project, 'form': form, 'errorMsg': errorMsg})


# no encore termine
@login_required
def add(request):
    active_project = request.session.get('active_project', False)
    if active_project:
        project = get_object_or_404(Project, pk=active_project)
        if request.method == 'POST':
            form = ProjectVulnForm(request.POST, project=active_project)
            if form.is_valid():
                vuln = VulnInst()
                vuln.base_pk = None
                vuln.create_user = request.user
                vuln.ref = form.cleaned_data.get('ref')
                vuln.vulnerability = form.cleaned_data.get('vulnerability')
                vuln.description = form.cleaned_data.get('description')
                vuln.recommendation = form.cleaned_data.get('recommendation')
                vuln.type = form.cleaned_data.get('type')
                vuln.nature = form.cleaned_data.get('nature')
                vuln.category = form.cleaned_data.get('category')

                vuln.exploitation_impact = form.cleaned_data.get('exploitation_impact')
                vuln.exploitation_complexity = form.cleaned_data.get('exploitation_complexity')
                vuln.action_complexity = form.cleaned_data.get('action_complexity')

                vuln.project = project
                vuln.save()

                # adding feed
                add_p_vuln_post = ''.join([ u'<span class="glyphicon glyphicon-flag"> </span> ',
                                        _("Add unexisting Vulnerability"),
                                        u' <a href="/projects/show/{0}/">{1}</a>'.format( vuln.pk, vuln.vulnerability),
                                        _("to Project"),
                                        u' <a href="/projects/{0}/">{1}</a> .'.format(project.slug, project.project)])
                feed = Feed(user=request.user, post=add_p_vuln_post)
                feed.save()
                #addiing notifications
                request.user.profile.notify_Adding_vuln_to_project(vuln, project)

                # adding tags
                tags = form.cleaned_data.get('tags')
                vuln.create_tags(tags)

                return redirect('/projects/' + project.slug)

            tagsliste = [tag[1:-1] for tag in request.POST['tags'][1:-1].split(",")]
            tags = [i.name for i in Tag.objects.all()]
        else:

            tagsliste = []
            form = ProjectVulnForm(project=active_project)
            tags = [i.name for i in Tag.objects.all()]

        return render(request, 'projects/add.html', {'tags': tags, 'form': form, 'tagsliste': tagsliste})
    return redirect('/projects/')


@login_required
def show_vuln(request, pk):
    vuln = get_object_or_404(VulnInst, pk=pk)
    active_project = request.session.get('active_project', False)
    project = get_object_or_404(Project, pk=active_project)
    return render(request, 'projects/vuln.html', {'vuln': vuln, 'project': project})


@login_required
def edit(request, id):
    if id:
        vuln = get_object_or_404(VulnInst, pk=id)
        vuln.update_user = request.user
        active_project = request.session.get('active_project', False)
        active_project_slug = request.session.get('active_project_slug', False)
        project = get_object_or_404(Project, pk=active_project)

    else:
        vuln = VulnInst(create_user=request.user)

    if request.POST:
        form = ProjectVulnForm(request.POST, instance=vuln, project=project.id)
        if form.is_valid():
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

            # add tags
            vuln.tagsproject.through.objects.filter(vulninst__id=vuln.id).delete()
            tags = form.cleaned_data.get('tags')
            vuln.create_tags(tags)
            vuln.save()
            edit_p_vuln_post = ''.join([ u'<span class="glyphicon glyphicon-refresh"> </span> ',
                                        _("Edit a Vulnerability"),
                                        u' <a href="/projects/show/{0}/">{1}</a>'.format( vuln.pk, vuln.vulnerability),
                                        _("from Project"),
                                        u' <a href="/projects/{0}/">{1}</a> .'.format(project.slug, project.project)])

            feed = Feed(user=request.user, post=edit_p_vuln_post)
            feed.save()
            return redirect('/projects/' + active_project_slug)
        tagsliste = [tag[1:-1] for tag in request.POST['tags'][1:-1].split(",")]
    else:
        tagsliste = vuln.get_items_tags()
        form = ProjectVulnForm(project=project.id, instance=vuln)

    tags = [i.name for i in Tag.objects.all()]
    return render(request, 'projects/edit.html',
                  {'tags': tags, 'tagsliste': tagsliste, 'form': form, 'project': project})


@login_required
def delete(request, id):
    if id:
        vuln = get_object_or_404(VulnInst, pk=id)
        active_project = request.session.get('active_project', False)
        active_project_slug = request.session.get('active_project_slug', False)
        project = get_object_or_404(Project, pk=active_project)
        if vuln.project.pk == active_project:
            delete_p_vuln_post = ''.join([ u'<span class="glyphicon glyphicon-trash"> </span> ',
                                        _("Remove a Vulnerability"),
                                        u' <b>{0}</b>'.format(vuln.vulnerability),
                                        _("from Project"),
                                        u' <a href="/projects/{0}/">{1}</a> .'.format(project.slug, project.project)])
            feed = Feed(user=request.user, post=delete_p_vuln_post)
            feed.save()
            vuln.delete()
    return redirect('/projects/' + active_project_slug)


# Project Client managment

@login_required
def add_client(request):
    data = {}
    if request.method == 'POST':  # and request.is_ajax():
        form = ClientForm(request.POST)
        if form.is_valid():
            client = Client()
            client.name = form.cleaned_data.get('name')
            client.save()
            add_client_post = ''.join([ u'<span class="glyphicon glyphicon-plus"> </span> ',
                                        _("Add a new Client"),
                                        u' <b>{0}</b>'.format(client.name)])
            feed = Feed(user=request.user, post=add_client_post)
            feed.save()
            data['new_item_value'] = client.name;
            data['new_item_key'] = client.pk;
            data['stat'] = "ok";
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error";
            return render(request, 'projects/add_client_modal.html', {'form': form})
    else:
        form = ClientForm()
        return render(request, 'projects/add_client_modal.html', {'form': form})


@login_required
def client(request, id):
    if id:
        client = get_object_or_404(Client, pk=id)
        request.session['active_client'] = client.pk
        projects = Project.objects.filter(client=client)
        uploaded_picture = False
        try:
            if request.GET.get('upload_picture') == 'uploaded':
                uploaded_picture = True
        except Exception, e:
            pass

        return render(request, 'projects/client.html',
                      {'client_projects': projects, 'client': client, 'uploaded_picture': uploaded_picture})

    return redirect('/projects')


@login_required
def c_upload_picture(request):
    try:
        active_client = request.session.get('active_client', False)
        profile_pictures = django_settings.MEDIA_ROOT + '/client_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + str(active_client) + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)
        return redirect('/projects/client/{0}/?upload_picture=uploaded'.format(active_client))
    except Exception, e:
        try:
            return redirect('/projects/client/{0}/'.format(active_client))
        except Exception, e:
            return redirect('/projects')


@login_required
def c_save_uploaded_picture(request):
    try:
        active_client = request.session.get('active_client', False)

        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/client_pictures/{0}_tmp.jpg'.format(active_client)
        filename = django_settings.MEDIA_ROOT + '/client_pictures/{0}.jpg'.format(active_client)
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
        return redirect('/projects/client/{0}/'.format(active_client))
    except Exception, e:
        pass
    return redirect('/projects/')


#Project Stat

@login_required
def chart_data_json(request):
    data = {}
    params = request.GET

    days = ''
    name = params.get('name', '')
    active_project = request.session.get('active_project', False)

    if name == 'dst_by_severity':
        data['chart_data'] = ChartData.get_dst_by_severity(active_project)


    elif name == 'dst_by_type':
        data['chart_data'] = ChartData.get_dst_by_type(active_project)

    elif name == 'dst_by_action_prio':
        data['chart_data'] = ChartData.get_dst_by_AP(active_project)

    elif name == 'dst_by_action_compl':
        data['chart_data'] = ChartData.get_dst_by_AC(active_project)

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def project_action_edit(request, id, action):
    etat = 'severity'
    project_id = request.session['active_project']
    if action == 'exploitation_impact':
        instance = ProjectExploitation_impact.objects.get(id=id)
        form = ProjectExploitationImpactForm(request.POST or None, instance=instance)
    elif action == 'action_complexity':
        instance = ProjectAction_complexity.objects.get(id=id)
        form = ProjectActionComplexityForm(request.POST or None, instance=instance)
        etat = 'priority'
    elif action == 'exploitation_complexity':
        instance = ProjectExploitation_complexity.objects.get(id=id)
        form = ProjectExploitationComplexityForm(request.POST or None, instance=instance)
    elif action == 'action_priority':
        instance = ProjectAction_priority.objects.get(id=id)
        form = ProjectActionPriorityForm(request.POST or None, instance=instance)
        etat = 'priority'
    elif action == 'severity':
        instance = ProjectSeverity.objects.get(id=id)
        form = ProjectSeverityForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.update(id=id)

        return redirect('preferences_project', etat=etat, project_id=project_id)
    return render(request, 'projects/matrixproject/project_edit_action.html', {'action': action, 'form': form})


#update
@login_required
def project_action_add(request, action):
    etat = 'severity'
    project_id = request.session['active_project']
    if action == 'exploitation_impact':
        form = ProjectExploitationImpactForm(request.POST or None)
    elif action == 'action_complexity':
        form = ProjectActionComplexityForm(request.POST or None)
        etat = 'priority'
    elif action == 'exploitation_complexity':
        form = ProjectExploitationComplexityForm(request.POST or None)
    elif action == 'action_priority':
        form = ProjectActionPriorityForm(request.POST or None)
        etat = 'priority'
    elif action == 'severity':
        form = ProjectSeverityForm(request.POST or None)
    if form.is_valid():
        form.save(project_id=project_id)

        return redirect('preferences_project', etat=etat, project_id=project_id)
    return render(request, 'projects/matrixproject/project_add_action.html', {'action': action, 'form': form})


@login_required
def project_action_delete(request, id, action):
    etat = 'severity'
    if action == 'exploitation_impact':
        exploitation_impact = ProjectExploitation_impact.objects.get(id=id)
        exploitation_impact.delete()
    elif action == 'action_complexity':
        action_complexity = ProjectAction_complexity.objects.get(id=id)
        action_complexity.delete()
        etat = 'priority'
    elif action == 'exploitation_complexity':
        exploitation_complexity = ProjectExploitation_complexity.objects.get(id=id)
        exploitation_complexity.delete()
    elif action == 'action_priority':
        action_priority = ProjectAction_priority.objects.get(id=id)
        action_priority.delete()
        etat = 'priority'
    elif action == 'severity':
        severity = ProjectSeverity.objects.get(id=id)
        severity.delete()
    project_id = request.session['active_project']
    return redirect('preferences_project', etat=etat, project_id=project_id)


@login_required
@ajax_required
def preview_vuln(request):
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
