from nicegui import ui, app
from typing import Dict, Any, Optional

def create_navbar(cart_service):
    """Create the navigation bar for the application"""
    with ui.header().classes('bg-white shadow-md'):
        with ui.row().classes('w-full max-w-screen-xl mx-auto items-center justify-between p-4'):
            # Logo and brand
            with ui.link('/', new_tab=False).classes('no-underline text-inherit'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('watch').classes('text-3xl text-blue-600')
                    ui.label('Luxury Watch Store').classes('text-2xl font-bold')
            
            # Navigation links
            with ui.row().classes('gap-6 items-center'):
                ui.link('Home', '/').classes('text-lg hover:text-blue-600 transition-colors')
                
                # Categories dropdown
                with ui.link('').classes('text-lg hover:text-blue-600 transition-colors'):
                    ui.label('Categories')
                    ui.icon('expand_more')
                    
                    with ui.menu().classes('min-w-40'):
                        ui.menu_item('Luxury Watches', lambda: ui.navigate('/'))
                        ui.menu_item('Sports Watches', lambda: ui.navigate('/'))
                        ui.menu_item('Smart Watches', lambda: ui.navigate('/'))
                        ui.menu_item('Vintage Watches', lambda: ui.navigate('/'))
                
                ui.link('About', '/').classes('text-lg hover:text-blue-600 transition-colors')
                ui.link('Contact', '/').classes('text-lg hover:text-blue-600 transition-colors')
                
                # Cart button with badge
                with ui.button(icon='shopping_cart', on_click=lambda: ui.navigate('/cart')).classes('ml-4'):
                    cart_badge = ui.badge(str(cart_service.get_item_count()), color='red').classes('text-white')
                    
                    # Update badge when cart changes
                    @app.on('cart_updated')
                    def update_cart_badge():
                        cart_badge.set_text(str(cart_service.get_item_count()))
                        if cart_service.get_item_count() > 0:
                            cart_badge.classes('text-white')
                        else:
                            cart_badge.classes('text-white opacity-0')

def create_footer():
    """Create the footer for the application"""
    with ui.footer().classes('bg-gray-800 text-white mt-auto'):
        with ui.column().classes('w-full max-w-screen-xl mx-auto p-8'):
            with ui.grid(columns=4).classes('w-full gap-8'):
                # Company info
                with ui.column().classes('gap-2'):
                    ui.label('Luxury Watch Store').classes('text-xl font-bold mb-4')
                    ui.label('We offer the finest selection of luxury timepieces from renowned brands around the world.')
                    
                    with ui.row().classes('gap-4 mt-4'):
                        for icon in ['facebook', 'twitter', 'instagram', 'youtube']:
                            ui.button(icon=icon, color='white').props('flat round')
                
                # Quick links
                with ui.column().classes('gap-2'):
                    ui.label('Quick Links').classes('text-xl font-bold mb-4')
                    for link in ['Home', 'About Us', 'Contact', 'FAQ', 'Terms & Conditions', 'Privacy Policy']:
                        ui.link(link, '/').classes('text-gray-300 hover:text-white transition-colors')
                
                # Categories
                with ui.column().classes('gap-2'):
                    ui.label('Categories').classes('text-xl font-bold mb-4')
                    for category in ['Luxury Watches', 'Sports Watches', 'Smart Watches', 'Vintage Watches', 'Watch Accessories']:
                        ui.link(category, '/').classes('text-gray-300 hover:text-white transition-colors')
                
                # Contact
                with ui.column().classes('gap-2'):
                    ui.label('Contact Us').classes('text-xl font-bold mb-4')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('location_on')
                        ui.label('123 Watch Avenue, New York, NY 10001')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('phone')
                        ui.label('+1 (555) 123-4567')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('email')
                        ui.label('info@luxurywatchstore.com')
            
            ui.separator().classes('my-6')
            
            with ui.row().classes('w-full justify-between items-center'):
                ui.label('© 2023 Luxury Watch Store. All rights reserved.')
                
                with ui.row().classes('gap-4'):
                    for payment in ['visa', 'mastercard', 'amex', 'paypal']:
                        ui.image(f'/static/payment/{payment}.png').classes('h-8')

def create_product_card(product: Dict[str, Any], cart_service, container: Optional[ui.element] = None):
    """Create a product card for the given product"""
    container_element = container or ui
    
    with container_element:
        with ui.card().classes('w-full h-full flex flex-col'):
            # Product image
            with ui.link(f'/product/{product["id"]}'):
                ui.image(f'/static/watches/{product["image"]}').classes('w-full h-48 object-contain')
            
            with ui.card_section().classes('flex-grow'):
                ui.link(product['name'], f'/product/{product["id"]}').classes('text-lg font-semibold hover:text-blue-600')
                ui.label(product['brand']).classes('text-sm text-gray-600')
                ui.label(f"${product['price']:,.2f}").classes('text-lg font-bold text-blue-600 mt-2')
                
                # Truncated description
                description = product['description']
                if len(description) > 100:
                    description = description[:97] + '...'
                ui.label(description).classes('text-sm text-gray-700 mt-2')
            
            with ui.card_actions().classes('justify-between items-center'):
                ui.link('Details', f'/product/{product["id"]}').classes('text-blue-600 hover:underline')
                
                def add_to_cart():
                    cart_service.add_item(product, 1)
                    ui.notify(f"Added {product['name']} to cart", color='positive')
                
                ui.button(icon='add_shopping_cart', on_click=add_to_cart).props('flat color=primary').tooltip('Add to Cart')