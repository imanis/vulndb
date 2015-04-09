from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from vulnDB.reports.forms import *
from vulnDB.feeds.models import Feed
from vulnDB.projects.models import Project
from vulnDB.reports.models import *
from django.shortcuts import redirect
from django.http import HttpResponse
import json
from export_scripts.generate_docx import generate_docx
from cStringIO import StringIO
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def select_template(request, id):
    template = ReportTemplate.objects.get(id=id)
    return render(request, 'reports/select_template.\
                  html', {'template': template})



@login_required
def add_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            add_template_post = u'<span class="glyphicon glyphicon-plus">{0}</span> Add a new Template <b>{1}</b> .' \
                .format(request.user, form.cleaned_data.get('name'))
            feed = Feed(user=request.user, post=add_template_post)
            feed.save()

            template = form.save()
            template.create_user=request.user
            template.save()
            return redirect('templates')

    instance = ReportTemplateStandart.objects.get(id=1)
    data={'front_cover':instance.front_cover,
    'header':instance.header,
    'footer':instance.footer,
    'font':instance.font,
    'font_size':instance.font_size,




    }
    form = TemplateForm(data)
    return render(request,
                  'reports/template/add_template.html', {'form': form})


@login_required
def add_frontcover(request):
    data = {}
    if request.method == 'POST':  # and request.is_ajax():
        form = FrontCoverPageForm(request.POST)
        if form.is_valid():
            frontcover = TemplateFrontCoverPage()
            frontcover.name = form.cleaned_data.get('name')
            frontcover.content = form.cleaned_data.get('content')

            frontcover.save()
            add_frontcover_post = u'<span class="glyphicon glyphicon-plus"></span> Add a new Front cover <b>{1}</b> .' \
                .format(request.user, frontcover.name)
            feed = Feed(user=request.user, post=add_frontcover_post)
            feed.save()
            data['new_item_value'] = frontcover.name
            data['new_item_key'] = frontcover.pk
            data['stat'] = "ok"
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error"
            return render(request, 'reports/template/partial_front\
                          cover.html', {'form': form})
    else:
        form = FrontCoverPageForm()
        return render(request, 'reports/template/partial_frontcover.html',
                      {'form': form})


@login_required
def add_font(request):
    data = {}
    if request.method == 'POST':  # and request.is_ajax():
        form = FontForm(request.POST)
        if form.is_valid():
            font = TemplateFont()
            font.name = form.cleaned_data.get('name')
            font.save()
            add_font_post = u'<span class="glyphicon glyphicon-plus"></span> Add a new Font <b>{1}</b> .' \
                .format(request.user, font.name)
            feed = Feed(user=request.user, post=add_font_post)
            feed.save()
            data['new_item_value'] = font.name
            data['new_item_key'] = font.pk
            data['stat'] = "ok"
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error"
            return render(request, 'reports/template/partial_font.html',
                          {'form': form})
    else:
        form = FontForm()
        return render(request, 'reports/template/partial_font.html',
                      {'form': form})


@login_required
def add_footer(request):
    data = {}
    if request.method == 'POST':  # and request.is_ajax():
        form = FooterForm(request.POST)
        if form.is_valid():
            footer = TemplateFooter()
            footer.name = form.cleaned_data.get('name')
            footer.content = form.cleaned_data.get('content')
            footer.save()
            add_footer_post = u'<span class="glyphicon glyphicon-plus"></span> Add a new Footer <b>{1}</b> .' \
                .format(request.user, footer.name)
            feed = Feed(user=request.user, post=add_footer_post)
            feed.save()
            data['new_item_value'] = footer.name
            data['new_item_key'] = footer.pk
            data['stat'] = "ok"
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error"
            return render(request, 'reports/template/partial_footer.html',
                          {'form': form})
    else:
        form = FooterForm()
        return render(request, 'reports/template/partial_footer.html',
                      {'form': form})


@login_required
def add_header(request):
    data = {}
    if request.method == 'POST':  # and request.is_ajax():
        form = HeaderForm(request.POST)
        if form.is_valid():
            header = TemplateHeader()
            header.name = form.cleaned_data.get('name')
            header.content = form.cleaned_data.get('content')
            header.save()
            add_header_post = u'<span class="glyphicon glyphicon-plus"></span> Add a new Header <b>{1}</b> .' \
                .format(request.user, header.name)
            feed = Feed(user=request.user, post=add_header_post)
            feed.save()
            data['new_item_value'] = header.name
            data['new_item_key'] = header.pk
            data['stat'] = "ok"
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error"
            return render(request, 'reports/template/partial_header.html',
                          {'form': form})
    else:
        form = HeaderForm()
        return render(request, 'reports/template/partial_header.html',
                      {'form': form})


@login_required
def add_font_size(request):
    data = {}
    if request.method == 'POST':  # and request.is_ajax():
        form = FontSizeForm(request.POST)
        if form.is_valid():
            font_size = TemplateFontSize()
            font_size.size = form.cleaned_data.get('size')
            font_size.save()
            add_font_size_post = u'<span class="glyphicon glyphicon-plus"></span> Add a new Font Size <b>{1}</b> .' \
                .format(request.user, font_size.size)
            feed = Feed(user=request.user, post=add_font_size_post)
            feed.save()
            data['new_item_value'] = font_size.size
            data['new_item_key'] = font_size.pk
            data['stat'] = "ok"
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error"
            return render(request, 'reports/template/partial_fontsize.html',
                          {'form': form})
    else:
        form = FontSizeForm()
        return render(request, 'reports/template/partial_fontsize.html',
                      {'form': form})


@login_required
def delete_template(request, id):
    template = ReportTemplate.objects.get(id=id)
    template.delete()
    return redirect('templates')


@login_required
def edite_template(request, id):
    instance = ReportTemplate.objects.get(id=id)
    form = TemplateForm(request.POST or None, instance=instance)
    if form.is_valid():
        template = form.save()
        template.update_user=request.user
        template.update_date=datetime.now()
        template.save()
        return redirect('templates')
    return render(request, 'reports/template/edit_template.html',
                  {'form': form})


@login_required
def reports(request):
    reports = Report.get_reports()
    templates = ReportTemplate.get_templates()
    return render(request, 'reports/reports.html', {'reports': reports,
                  'active': 'reports'})


@login_required
def templates(request):
    templates = ReportTemplate.get_templates()
    paginator = Paginator(templates, 12)
    page = request.GET.get('page')
    try:
        templates = paginator.page(page)
    except PageNotAnInteger:
        templates = paginator.page(1)
    except EmptyPage:
        templates = paginator.page(paginator.num_pages)
    return render(request, 'reports/templates.html', {'templates': templates,
                  'active': 'templates'})

@login_required
def add_report(request):
    if request.method == 'POST':
        form = ReportsForm(request.POST)
        if form.is_valid():
            add_report_post = u'<span class="glyphicon glyphicon-plus">{0}</span> Add a new Report <b>{1}</b> .' \
                .format(request.user, form.cleaned_data.get('name'))
            feed = Feed(user=request.user, post=add_report_post)
            feed.save()
            report = form.save()
            report.create_user=request.user
            report.save()
            return redirect('reports')

    form = ReportsForm()
    # contactform=ContactForm()
    return render(request, 'reports/add_report.html', {'form': form})


@login_required
def add_contact(request):
    data = {}
    if request.method == 'POST':  # and request.is_ajax():
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = ReportContact()
            contact.name = form.cleaned_data.get('name')
            contact.email = form.cleaned_data.get('email')
            contact.phones = form.cleaned_data.get('phones')
            contact.save()
            add_contact_post = u'<span class="glyphicon glyphicon-plus"></span> Add a new Contact <b>{1}</b> .' \
                .format(request.user, contact.name)
            feed = Feed(user=request.user, post=add_contact_post)
            feed.save()
            data['new_item_value'] = contact.name
            data['new_item_key'] = contact.pk
            data['stat'] = "ok"
            return HttpResponse(json.dumps(data), mimetype="application/json")
        else:
            data['stat'] = "error"
            return render(request, 'reports/partial_contact.html',
                          {'form': form})
    else:
        form = ContactForm()
        return render(request, 'reports/partial_contact.html', {'form': form})


@login_required
def delete_report(request, id):
    report = Report.objects.get(id=id)
    report.delete()
    return redirect('reports')


@login_required
def edite_report(request, id):
    instance = Report.objects.get(id=id)
    form = ReportsForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('reports')
    return render(request, 'reports/edit_report.html', {'form': form})


@login_required
def generate(request, id):

    project = get_object_or_404(Project, pk=id)


    # call scipt
    document = generate_docx(id)

    f = StringIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = ''.join(['attachment; filename=', project.slug, '_', project.client.name,'.docx'])
    response['Content-Length'] = length
    return response

   # return redirect('reports')

@login_required
def add_template_standart(request):
    if request.method == 'POST':
        form = TemplateStandartForm(request.POST)
        if form.is_valid():
            add_template_post = u'<span class="glyphicon glyphicon-plus">{0}</span> Add a standart Template <b>{1}</b> .' \
                .format(request.user, form.cleaned_data.get('name'))
            feed = Feed(user=request.user, post=add_template_post)
            feed.save()
            template = form.save()
            template.create_user=request.user
            template.save()
            return redirect('templates')
    form = TemplateStandartForm()
    return render(request,
                  'reports/template/add_template_standart.html', {'form': form})


@login_required
def edite_template_standart(request):
    instance = ReportTemplateStandart.objects.get(id=1)
    form = TemplateStandartForm(request.POST or None, instance=instance)
    if form.is_valid():
        template = form.save()
        template.update_user=request.user
        template.update_date=datetime.now()
        template.save()
        return redirect('templates')
    return render(request, 'reports/template/edit_template_standart.html',
                  {'form': form})
