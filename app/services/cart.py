from typing import Dict, List, Any
from nicegui import app

class CartService:
    """Service for managing the shopping cart"""
    
    def __init__(self):
        """Initialize an empty shopping cart"""
        self._items: List[Dict[str, Any]] = []
    
    def add_item(self, product: Dict[str, Any], quantity: int = 1) -> None:
        """
        Add a product to the cart
        
        Args:
            product: The product to add
            quantity: The quantity to add (default: 1)
        """
        # Check if product is already in cart
        existing_item = next((item for item in self._items if item['product']['id'] == product['id']), None)
        
        if existing_item:
            # Update quantity if product already exists in cart
            existing_item['quantity'] += quantity
        else:
            # Add new item to cart
            self._items.append({
                'product': product,
                'quantity': quantity
            })
        
        # Emit event to notify UI components
        app.storage.user['cart_items'] = self._items
        app.broadcast('cart_updated')
    
    def update_quantity(self, product_id: int, quantity: int) -> None:
        """
        Update the quantity of a product in the cart
        
        Args:
            product_id: The ID of the product to update
            quantity: The new quantity
        """
        for item in self._items:
            if item['product']['id'] == product_id:
                item['quantity'] = max(1, quantity)  # Ensure quantity is at least 1
                break
        
        # Emit event to notify UI components
        app.storage.user['cart_items'] = self._items
        app.broadcast('cart_updated')
    
    def remove_item(self, product_id: int) -> None:
        """
        Remove a product from the cart
        
        Args:
            product_id: The ID of the product to remove
        """
        self._items = [item for item in self._items if item['product']['id'] != product_id]
        
        # Emit event to notify UI components
        app.storage.user['cart_items'] = self._items
        app.broadcast('cart_updated')
    
    def get_items(self) -> List[Dict[str, Any]]:
        """
        Get all items in the cart
        
        Returns:
            List of cart items
        """
        return self._items
    
    def get_item_count(self) -> int:
        """
        Get the total number of items in the cart
        
        Returns:
            Total number of items
        """
        return sum(item['quantity'] for item in self._items)
    
    def get_total_price(self) -> float:
        """
        Get the total price of all items in the cart
        
        Returns:
            Total price
        """
        return sum(item['product']['price'] * item['quantity'] for item in self._items)
    
    def clear(self) -> None:
        """Clear all items from the cart"""
        self._items = []
        
        # Emit event to notify UI components
        app.storage.user['cart_items'] = self._items
        app.broadcast('cart_updated')