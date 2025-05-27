from nicegui import ui, app
from app.data.products import watches
from app.frontend.components import create_navbar, create_footer, create_product_card
from app.services.cart import CartService

# Initialize the cart service
cart_service = CartService()

# Main page - Product listing
@ui.page('/')
def home_page():
    create_navbar(cart_service)
    
    with ui.column().classes('w-full max-w-screen-xl mx-auto p-4'):
        ui.label('Luxury Watches').classes('text-3xl font-bold my-4')
        
        # Filters
        with ui.row().classes('w-full gap-4 my-4'):
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-4'):
                    ui.label('Filter:').classes('text-lg')
                    
                    brand_filter = ui.select(
                        options=['All Brands'] + sorted(list({w['brand'] for w in watches})),
                        value='All Brands',
                        label='Brand'
                    ).classes('min-w-40')
                    
                    price_range = ui.select(
                        options=['All Prices', 'Under $1,000', '$1,000 - $5,000', '$5,000 - $10,000', 'Over $10,000'],
                        value='All Prices',
                        label='Price Range'
                    ).classes('min-w-40')
                    
                    sort_by = ui.select(
                        options=['Featured', 'Price: Low to High', 'Price: High to Low', 'Name: A-Z'],
                        value='Featured',
                        label='Sort By'
                    ).classes('min-w-40')
        
        # Product grid
        product_grid = ui.grid(columns=3).classes('gap-4 w-full')
        
        def update_products():
            # Clear existing products
            product_grid.clear()
            
            # Filter products
            filtered_watches = watches
            
            # Apply brand filter
            if brand_filter.value != 'All Brands':
                filtered_watches = [w for w in filtered_watches if w['brand'] == brand_filter.value]
            
            # Apply price filter
            if price_range.value == 'Under $1,000':
                filtered_watches = [w for w in filtered_watches if w['price'] < 1000]
            elif price_range.value == '$1,000 - $5,000':
                filtered_watches = [w for w in filtered_watches if 1000 <= w['price'] < 5000]
            elif price_range.value == '$5,000 - $10,000':
                filtered_watches = [w for w in filtered_watches if 5000 <= w['price'] < 10000]
            elif price_range.value == 'Over $10,000':
                filtered_watches = [w for w in filtered_watches if w['price'] >= 10000]
            
            # Apply sorting
            if sort_by.value == 'Price: Low to High':
                filtered_watches = sorted(filtered_watches, key=lambda w: w['price'])
            elif sort_by.value == 'Price: High to Low':
                filtered_watches = sorted(filtered_watches, key=lambda w: w['price'], reverse=True)
            elif sort_by.value == 'Name: A-Z':
                filtered_watches = sorted(filtered_watches, key=lambda w: w['name'])
            
            # Display products
            for watch in filtered_watches:
                create_product_card(watch, cart_service, product_grid)
            
            # Show message if no products match filters
            if not filtered_watches:
                with product_grid:
                    ui.label('No watches match your selected filters').classes('text-xl text-gray-500 col-span-3 text-center py-8')
        
        # Update products when filters change
        brand_filter.on('change', update_products)
        price_range.on('change', update_products)
        sort_by.on('change', update_products)
        
        # Initial product display
        update_products()
    
    create_footer()

# Product detail page
@ui.page('/product/{product_id}')
def product_detail(product_id: str):
    try:
        product_id = int(product_id)
        watch = next((w for w in watches if w['id'] == product_id), None)
        
        if not watch:
            return ui.navigate('/')
        
        create_navbar(cart_service)
        
        with ui.column().classes('w-full max-w-screen-xl mx-auto p-4'):
            # Breadcrumb navigation
            with ui.row().classes('w-full mb-4'):
                with ui.link('Home', '/').classes('text-blue-500 hover:underline'):
                    ui.icon('home').classes('mr-1')
                ui.label('›').classes('mx-2')
                ui.label(watch['brand']).classes('text-gray-600')
                ui.label('›').classes('mx-2')
                ui.label(watch['name']).classes('text-gray-800')
            
            # Product details
            with ui.row().classes('w-full gap-8'):
                # Product image
                with ui.card().classes('w-1/2'):
                    ui.image(f'/static/watches/{watch["image"]}').classes('w-full h-auto object-contain')
                
                # Product info
                with ui.card().classes('w-1/2 p-6'):
                    ui.label(watch['name']).classes('text-2xl font-bold')
                    ui.label(watch['brand']).classes('text-xl text-gray-600 mb-4')
                    ui.label(f"${watch['price']:,.2f}").classes('text-xl font-bold text-blue-600 mb-4')
                    
                    ui.separator()
                    
                    ui.label('Description').classes('text-lg font-semibold mt-4')
                    ui.label(watch['description']).classes('text-gray-700 mb-4')
                    
                    ui.label('Specifications').classes('text-lg font-semibold mt-4')
                    with ui.row().classes('w-full gap-8 mb-4'):
                        with ui.column().classes('w-1/2'):
                            for key, value in [
                                ('Movement', watch['specs']['movement']),
                                ('Case Material', watch['specs']['case_material']),
                                ('Water Resistance', watch['specs']['water_resistance'])
                            ]:
                                with ui.row().classes('w-full mb-2'):
                                    ui.label(f"{key}:").classes('font-semibold')
                                    ui.label(value).classes('ml-2')
                        
                        with ui.column().classes('w-1/2'):
                            for key, value in [
                                ('Case Size', watch['specs']['case_size']),
                                ('Strap Material', watch['specs']['strap_material']),
                                ('Features', ', '.join(watch['specs']['features']))
                            ]:
                                with ui.row().classes('w-full mb-2'):
                                    ui.label(f"{key}:").classes('font-semibold')
                                    ui.label(value).classes('ml-2')
                    
                    ui.separator()
                    
                    with ui.row().classes('w-full items-center gap-4 mt-6'):
                        quantity = ui.number(value=1, min=1, max=10).classes('w-20')
                        
                        def add_to_cart():
                            cart_service.add_item(watch, quantity.value)
                            ui.notify(f"Added {quantity.value} × {watch['name']} to cart", color='positive')
                        
                        ui.button('Add to Cart', on_click=add_to_cart).props('color=primary icon=shopping_cart').classes('text-lg')
            
            # Related products
            ui.label('You May Also Like').classes('text-2xl font-bold mt-8 mb-4')
            with ui.grid(columns=4).classes('gap-4 w-full'):
                related_watches = [w for w in watches if w['brand'] == watch['brand'] and w['id'] != watch['id']]
                if not related_watches:
                    related_watches = [w for w in watches if w['id'] != watch['id']]
                
                for related in related_watches[:4]:  # Show up to 4 related products
                    create_product_card(related, cart_service)
        
        create_footer()
    except Exception as e:
        ui.notify(f"Error loading product: {str(e)}", color='negative')
        ui.navigate('/')

# Shopping cart page
@ui.page('/cart')
def cart_page():
    create_navbar(cart_service)
    
    with ui.column().classes('w-full max-w-screen-xl mx-auto p-4'):
        ui.label('Shopping Cart').classes('text-3xl font-bold my-4')
        
        cart_container = ui.column().classes('w-full')
        
        def update_cart_view():
            cart_container.clear()
            cart_items = cart_service.get_items()
            
            if not cart_items:
                with cart_container:
                    with ui.card().classes('w-full p-8 text-center'):
                        ui.label('Your cart is empty').classes('text-xl text-gray-500 mb-4')
                        ui.button('Continue Shopping', on_click=lambda: ui.navigate('/')).props('color=primary icon=shopping_bag')
                return
            
            with cart_container:
                # Cart items
                with ui.card().classes('w-full mb-4'):
                    with ui.column().classes('w-full'):
                        # Header
                        with ui.row().classes('w-full p-4 bg-gray-100 font-bold'):
                            ui.label('Product').classes('w-1/2')
                            ui.label('Price').classes('w-1/6 text-center')
                            ui.label('Quantity').classes('w-1/6 text-center')
                            ui.label('Total').classes('w-1/6 text-center')
                            ui.label('').classes('w-12')  # For remove button
                        
                        # Cart items
                        for item in cart_items:
                            with ui.row().classes('w-full p-4 border-b border-gray-200 items-center'):
                                # Product info
                                with ui.row().classes('w-1/2 items-center gap-4'):
                                    ui.image(f'/static/watches/{item["product"]["image"]}').classes('w-16 h-16 object-contain')
                                    with ui.column():
                                        ui.link(item['product']['name'], f'/product/{item["product"]["id"]}').classes('font-semibold hover:text-blue-600')
                                        ui.label(item['product']['brand']).classes('text-sm text-gray-600')
                                
                                # Price
                                ui.label(f"${item['product']['price']:,.2f}").classes('w-1/6 text-center')
                                
                                # Quantity
                                with ui.number(value=item['quantity'], min=1, max=10).classes('w-1/6 flex justify-center'):
                                    def on_quantity_change(e, item_id=item['product']['id']):
                                        cart_service.update_quantity(item_id, e.value)
                                        update_cart_view()
                                    
                                    _.on('update:model-value', on_quantity_change)
                                
                                # Total
                                ui.label(f"${item['product']['price'] * item['quantity']:,.2f}").classes('w-1/6 text-center font-semibold')
                                
                                # Remove button
                                with ui.button(icon='delete', color='negative', on_click=lambda id=item['product']['id']: remove_item(id)).classes('w-12'):
                                    _.tooltip('Remove item')
                
                # Order summary
                with ui.card().classes('w-full p-6'):
                    with ui.column().classes('w-full'):
                        ui.label('Order Summary').classes('text-xl font-bold mb-4')
                        
                        subtotal = sum(item['product']['price'] * item['quantity'] for item in cart_items)
                        shipping = 15.00 if subtotal < 100 else 0.00
                        tax = subtotal * 0.08  # 8% tax
                        total = subtotal + shipping + tax
                        
                        with ui.row().classes('w-full justify-between mb-2'):
                            ui.label('Subtotal:')
                            ui.label(f"${subtotal:,.2f}")
                        
                        with ui.row().classes('w-full justify-between mb-2'):
                            ui.label('Shipping:')
                            ui.label(f"${shipping:,.2f}" if shipping > 0 else "FREE")
                        
                        with ui.row().classes('w-full justify-between mb-2'):
                            ui.label('Tax (8%):')
                            ui.label(f"${tax:,.2f}")
                        
                        ui.separator()
                        
                        with ui.row().classes('w-full justify-between font-bold text-lg my-2'):
                            ui.label('Total:')
                            ui.label(f"${total:,.2f}")
                        
                        with ui.row().classes('w-full gap-4 mt-4'):
                            ui.button('Continue Shopping', on_click=lambda: ui.navigate('/')).props('outline icon=arrow_back')
                            
                            def checkout():
                                ui.notify('Checkout functionality would be implemented in a production version', color='info', timeout=5000)
                                # In a real app, this would redirect to a checkout page
                            
                            ui.button('Proceed to Checkout', on_click=checkout).props('color=primary icon=shopping_cart_checkout').classes('ml-auto')
        
        def remove_item(product_id):
            cart_service.remove_item(product_id)
            ui.notify('Item removed from cart', color='info')
            update_cart_view()
        
        # Initialize cart view
        update_cart_view()
        
        # Register for cart updates
        @app.on('cart_updated')
        def on_cart_updated():
            update_cart_view()
    
    create_footer()