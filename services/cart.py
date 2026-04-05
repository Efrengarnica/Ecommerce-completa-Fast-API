from repository.cart import CartRepository

class CartService:
    def __init__(self, repository: CartRepository):
        self.repository = repository
    
    

    async def create_cart_for_user(self, id: int):
        pass

  