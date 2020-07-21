"""pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import pharmadoc
from pharmadoc import urls
import changelog
from changelog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pharmadoc.views.start_view, name='startview'),
    path('all', pharmadoc.views.start_all_view, name='startallview'),
    path('submit/createsubmission', pharmadoc.views.createsubmission, name='createsubmission'),
    path('selectpharmacyforsubmitview/<int:primary_key>', pharmadoc.views.selectpharmacyforsubmitview, name='selectpharmacyforsubmitview'),
    path('submit/<int:primary_key>', pharmadoc.views.submit_view, name='submitview'),
    path('submissions/<int:primary_key>', pharmadoc.views.seesubmissions, name='seesubmissions'),
    path('allsubmissions/<int:primary_key>', pharmadoc.views.allsubmissions, name='allsubmissions'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('showorders/<int:primary_key>', pharmadoc.views.showorders, name='showorders'),
    path('password/reset', pharmadoc.views.change_password, name='change_password'),
    path('export', pharmadoc.views.exportcsv, name='exportcsv'), #mailalarm
    path('exportall', pharmadoc.views.exportcsv_all, name='exportcsv_all'),
    path('exportadvanced', pharmadoc.views.exportcsvadvanced, name='exportcsvadvanced'),
    path('changes/', changelog.views.changehistory, name='changes'),
    path('addorder/', pharmadoc.views.add_order, name='addorder'),
    path('addpharmacy/', pharmadoc.views.add_pharmacy, name='addpharmacy'),
    path('mix/selectordersformixedsubmission/', pharmadoc.views.selectordersformixedsubmission, name='selectordersformixedsubmission'),
    path('mix/selectmixedpharmacyforsubmitview/<int:primary_key>', pharmadoc.views.selectmixedpharmacyforsubmitview, name='selectmixedpharmacyforsubmitview'),
    path('mix/submitmixedsubmission', pharmadoc.views.submitmixedsubmission, name='submitmixedsubmission'),
    path('mix/createmixedsubmission', pharmadoc.views.createmixedsubmission, name='createmixedsubmission'),
    path('mix/selectmixedpharmacy', pharmadoc.views.selectmixedpharmacy, name='selectmixedpharmacy'), # select a mixed pharmacy to create a mixed solution
    path('mix/selectordersformixedpharmacy', pharmadoc.views.selectordersformixedpharmacy, name='selectordersformixedpharmacy'), # select the orders those are used to create a mixed solution
    path('mix/mixedsolutions', pharmadoc.views.mixed_solutions, name='overview mixed solution'),                    #shows mixed pharmacy which is active
    path('mix/allmixedsolutions', pharmadoc.views.all_mixed_solutions, name='full overview mixed solution'),        #shows mixed pharmacy wich can be deactive also
    path('mix/allsubmissions/<int:primary_key>', pharmadoc.views.allmixedsubmissions, name='allmixedsubmissions'),  #shows all submission concerning a mixed pharmacy
    path('mix/showmixedsolutions/<int:primary_key>', pharmadoc.views.showmixedsolutions, name='showmixedsolutions'),#shows all solutions concerning a mixed pharmacy
    path('mix/submissions/<int:primary_key>', pharmadoc.views.showmixedsubmissions, name='showmixedsubmissions'),   #shows all submissions concerning a mixed solutions
    path('mix/initmixedsolution', pharmadoc.views.initmixedsolution, name='initmixedsolution'),                     #Form to give details about the new mixed solution
    path('mix/addmixedsolution', pharmadoc.views.addmixedsolution, name='addmixedsolution'),                        #save new mixed solution dataset 
    path('mix/submit/<int:primary_key>', pharmadoc.views.mixedsubmit_view, name='mixedsubmitview'),                 #submit from a mixed solution
    path('mix/submit/createsubmission', pharmadoc.views.mixedcreatesubmission, name='mixedcreatesubmission'),       #save (mixed) submission
    path('order/', pharmadoc.views.order_view, name='showorders'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)