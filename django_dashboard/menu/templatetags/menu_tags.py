from django import template
from django.urls import reverse
from menu.models import MenuItem
from django.utils.safestring import mark_safe


register = template.Library()
@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
   request  = context['request']
   menus = MenuItem.objects.filter(menu_name =menu_name).select_related('parent').order_by('id')
   tree_menu = build_menu_tree(menus)
   active_url= request.path
   menu_html = render_menu(tree_menu, active_url)
   return mark_safe(menu_html)

def build_menu_tree(menus):
   tree ={}
   for menu in menus:
      menu.url = menu.url or reverse(menu.named_url) if menu.named_url else '#'
      tree.setdefault(menu.parent_id,[]).append(menu)
   return tree  


def render_menu(tree_menus,active_url,parent_id= None):
   items = tree_menus.get(parent_id,[])
   if not items:
      return  ''
   menu_str = '<ul class="list-none">'
   for item in items:
      children = render_menu(tree_menus,active_url,item.id)
      css_class= 'text-blue-500' if item.url == active_url else 'text-gray-700'
      menu_str += f'<li class="menu-item {css_class}"><a href="{item.url}">{item.name}</a>'
      if children:
            menu_str += f'<ul class="list-none" style="display:none">{children}</ul>'
     
   menu_str += '</ul>'
   return menu_str
  



   

