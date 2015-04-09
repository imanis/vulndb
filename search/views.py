from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from vulnDB.feeds.models import Feed
from vulnDB.projects.models import Project, VulnInst
from vulnDB.reports.models import Report
from vulnDB.vulns.models import Vuln
from vulnDB.projects.models import Client
from django.contrib.auth.decorators import login_required

@login_required
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')
        try:
            search_type = request.GET.get('type')
            if search_type not in ['feed', 'projects', 'clients', 'users', 'vulns', 'vulnsinst', 'reports']:
                search_type = 'feed'
        except Exception, e:
            search_type = 'feed'
        
        count = {}
        results = {}

        results['feed'] = Feed.objects.filter(post__icontains=querystring, parent=None)
        results['projects'] = Project.objects.filter(Q(project__icontains=querystring) | Q(nature__nature__icontains=querystring)|
                                                     Q(client__name__icontains=querystring))
        results['clients'] = Client.objects.filter(Q(name__icontains=querystring))
        results['users'] = User.objects.filter(Q(username__icontains=querystring) | Q(first_name__icontains=querystring) | Q(last_name__icontains=querystring))
        results['vulns'] = Vuln.objects.filter(Q(vulnerability__icontains=querystring) | Q(description__icontains=querystring)|
                                               Q(recommendation__icontains=querystring)| Q(nature__nature__icontains=querystring)|
                                               Q(create_user__username__icontains=querystring))
        results['vulnsinst'] = VulnInst.objects.filter(Q(vulnerability__icontains=querystring) | Q(description__icontains=querystring)|
                                               Q(recommendation__icontains=querystring)| Q(nature__nature__icontains=querystring)|
                                               Q(create_user__username__icontains=querystring))
        results['reports'] = Report.objects.filter(Q(name__icontains=querystring))



        count['feed'] = results['feed'].count()
        count['projects'] = results['projects'].count()
        count['clients'] = results['clients'].count()
        count['users'] = results['users'].count()
        count['vulns'] = results['vulns'].count()
        count['vulnsinst'] = results['vulnsinst'].count()
        count['reports'] = results['reports'].count()


        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type] })
    else:
        return render(request, 'search/search.html', { 'hide_search': True })
