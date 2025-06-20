from django import template
from django.urls import resolve
from tree_menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path_info
    
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    
    menu_tree = {}
    root_items = []
    
    for item in menu_items:
        if item.parent_id is None:
            root_items.append(item)
        menu_tree[item.id] = {
            'item': item,
            'children': [],
            'is_active': False,
            'is_expanded': False,
        }
    
    for item in menu_items:
        if item.parent_id:
            menu_tree[item.parent_id]['children'].append(menu_tree[item.id])
    
    active_item = None
    
    for item_id, item_data in menu_tree.items():
        item_url = item_data['item'].get_url()
        if item_url == current_url:
            item_data['is_active'] = True
            active_item = item_data
    
    if active_item:
        parent = active_item
        while parent:
            parent['is_expanded'] = True
            parent_id = parent['item'].parent_id
            parent = menu_tree.get(parent_id) if parent_id else None
    
    if active_item and active_item['children']:
        active_item['is_expanded'] = True
    
    def sort_items(items):
        return sorted(items, key=lambda x: x['item'].order)
    
    root_items = sort_items([menu_tree[item.id] for item in root_items])
    
    for item_data in menu_tree.values():
        item_data['children'] = sort_items(item_data['children'])
    
    return {
        'menu_name': menu_name,
        'menu_items': root_items,
        'current_url': current_url,
    }