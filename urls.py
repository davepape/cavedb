from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.showEntity, name='showEntity'),
    path('listentities', views.listEntities, name='listEntities'),
    path('addentityform', views.addEntityForm, name='addEntityForm'),
    path('addentity', views.addEntity, name='addEntity'),
    path('editentityform/<int:id>', views.editEntityForm, name='editEntityForm'),
    path('editentity', views.editEntity, name='editEntity'),
    path('addcategoryform', views.addCategoryForm, name='addCategoryForm'),
    path('addcategory', views.addCategory, name='addCategory'),
    path('searchform', views.searchForm, name='searchForm'),
    path('search', views.search, name='search'),
    path('searchname', views.searchName, name='searchName'),
    path('addlinkcategoryform', views.addLinkCategoryForm, name='addLinkCategoryForm'),
    path('addlinkcategory', views.addLinkCategory, name='addLinkCategory'),
    path('addlinkform/<int:id>', views.addLinkForm, name='addLinkForm'),
    path('addlink', views.addLink, name='addLink'),
    path('importcsvform', views.importCSVForm, name='importCSVForm'),
    path('importcsventities', views.importCSVEntities, name='importCSVEntities'),
    path('importcsvlinks', views.importCSVLinks, name='importCSVLinks'),
    path('exportcsventities', views.exportCSVEntities, name='exportCSVEntities'),
    path('exportcsvlinks', views.exportCSVLinks, name='exportCSVLinks'),
    path('graph', views.graph, name='graph'),
]
