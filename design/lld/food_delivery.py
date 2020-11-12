"""
https://github.com/mayankbansal93/lld-food-delivery-zomato-swiggy
UseCases:
  Restaurants can register themselves.
  Users can create, update, delete, get their profiles.
  User can search for the restaurant using a restaurant name, city name.
  Restaurants can add, update the food menu.
  User can see the food menu. User can get the food items based on Meal type or Cuisine type.
  User can add/remove items to/from the cart. User can get all the items of the cart.
  User can place or cancel the order. User can get all the orders ordered by him/her.
  User can apply the coupons. User can get the detailed bill containing tax details.
  User can make a payment using different modes of payment — credit card, wallet, etc.
  Delivery boy can get all the deliveries made by him using his Id.
  User can get the order status anytime. Success, Out for Delivery, Delivered, etc.
Constraints:

Basic Design:
  Services:
    Restaurant Service
    All the functionalities related to the restaurants will be handled by the Restaurant Service. It will interact with Restaurant Data only. It will render the first page of the application, i.e., the list of all restaurants or the searched restaurants. It will also allow restaurants to register and Admin to manage.
      addRestaurant # Restaurants can register themselves
      getAllRestaurants # Customers can see the list of all the restaurants
      getRestaurantById # Admin can search for the restaurant using Id 
      getRestaurantsByName # Customers can search for restaurants using name
      getRestaurantsByCity # Customers can search for restaurants using city
    User service:
    User profile related features will be provided by User Service. It will interact with User Data only. It will allow Customers and Delivery boys to register and update their profiles.
      addUser : Users can register themselves 
      deleteUser : Users can delete their profiles
      updateUser : Users can update their profiles
      getUser : Users can get info of their profiles
    Food Menu Service:
    Once the customer selected the restaurant, the second page of the application, i.e., the food menu will be rendered by the Food Menu Service. It will also allow customers to search for the items on the menu basis on some category. It will interact with Food Menu Data only.
      addMenuByRestaurantId : Restaurants can add the food menu.
      getMenuById : Admin can search for the food menu using Id.
      getMenuByRestaurantId : Customers can see the menu.
      addMenuItemsByMenuId : Admin can add more items in the menu
      addMenuItemsByRestaurantId : Restaurants can add more items. 
      getMenuItemsByRestaurantIdAndCuisine : Customers can search for the items using cuisine type. 
      getMenuItemsByRestaurantIdAndMealType : Customers can search for the items using meal type.
      getMenuItemById : Admin can search for the item using Id.
    Cart Service
    Cart Service will allow Customers to add or remove the items in or from the cart. It will render the third page of the application, i.e., items in the cart. It will interact with the Cart Data and will also call the Food Menu Service to get the items using Id. We can use the Command Pattern to handle the add or remove commands.
      updateCart : Customers can add/remove items. 
      clearCart : Customers can empty the cart. 
      getAllItemsOfCart : Customers can see the cart items.
    Pricing Service:
    Onthe cart page, Pricing Service will allow Customers to see the bill details. It will call the Cart Service to get all the items of the cart to render the bill. We can use a Strategy Pattern and have different types of strategies — TwentyPercentOff, FiveHundredOff, etc.
      getBill : Customers can see the bill details. 
    Order Service:
    Customers can place or cancel the order, once the cart is finalized, using Order Service. It will interact with Order Data only. It will allow customers to see the order history also. Customers can select the history based on the restaurant also. We can use the Command Pattern to handle place or cancel commands.
      updateOrder : Customers can place or cancel orders.
      getOrderById : Admin can search for the order. 
      getAllOrdersByRestautantId: Customers can see their order history for a restaurant.
      getAllOrders: Customers can see their all order history.
    
    Payment Service
    Payments can be made to the restaurants using Payment Service. It will interact with the Payment Data and also call the Pricing Service to validate the payment made & the Order Service to update the order status. It will allow Customers to add the Payment against their order.
      Customers can pay for their orders — addPayment
      Admin can search for the payment using Id — getPaymentById
      Customers can see the payment made — getPaymentByOrderId
      Payment must match the bill — validatePayment
    Delivery Service
    Delivery Service will deal with all the functionalities related to the order delivery. It will interact with the Delivery Data and also call the Order Service to get the order to be delivered.
      Admin/Restaurants can add delivery — addDelivery
      Admin can get the delivery by Id — getDeliveryById
      Delivery boy can see all the deliveries made — getDeliveriesByDeliveryBoyId
      Customers can track the order status — getOrderStatus
    
  Model Classes
    Restaurant
      Restaurant id — unique for each restaurant
      Restaurant name
      Address
    We can also add Review, Rating, Open-close timings.
    
    Address
      Address id — unique for each
      Address
      City
      Zipcode
      Location — can contain google maps link or longitude and latitude values.
    There is One-to-Many mapping from Address to Restaurant. For eg- restaurants in a mall.

    User
      User id — unique for each
      User name
      Phone no
      Address
    We can also add First name, Last name, Gender, Bio and some more details related to the user.
    
    Food Menu
      Food menu id — unique for each
      Restaurants ids — multiple
      Menu Items — multiple
    One-to-Many mapping from FoodMenu to Restaurant. For eg- Restaurant having franchises in multiple cities.
    
    Menu Item
      Menu Id — unique for each
      Name of Item
      Cuisine Type
      Meal Type
      Price
    We can also add Rating, Review of items, Number of times ordered a particular item
    
    Order
      Order id — unique for each order
      User id — who orders
      Restaurant id — orders from
      Menu Items to be ordered
      Status of Order
    
    Bill
      Bill Id — unique for each bill
      Total Cost of the Bill
      Discount applied
      Total tax
      Amount to be paid
    We can also add tax bifurcation — CGST, SGST for India. Discount bifurcation — card discount, coupon discount.
    
    Payment
      Payment Id — unique for each
      Order Id — for order details
      Amount Paid by user
      Coupon code applied
      Status of Payment
    
    Delivery
      Delivery Id — unique for each
      Delivery boy Id — User model
      User Id — for address details
      Order Id — for order details
      Delivery Time — for a status update
    We can also add feedback, ratings for the delivery.
    

    
BottleNeck:
Scalibility:

ALWAYS USE SOLID Principle
- Single-responsibility principle
  A class should only have a single responsibility, that is, only changes to one part of the software's specification should be able to affect the specification of the class.
- Open–closed principle
  "Software entities ... should be open for extension, but closed for modification."
- Liskov substitution principle
  "Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program."
  https://en.wikipedia.org/wiki/Design_by_contract
- Interface segregation principle
  "Many client-specific interfaces are better than one general-purpose interface."
- Dependency inversion principle
  One should "depend upon abstractions, [not] concretions."

"""