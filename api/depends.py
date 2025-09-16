# from api.internal.repository.payment import PaymentRepo
# from api.internal.repository.users import UsersRepo


# async def get_users_service() -> "UsersService":
#     from api.internal.services.users import UsersService
#     from api.internal.services.payment import PaymentService
    
#     payment_service = PaymentService(None, PaymentRepo())
#     users_service = UsersService(payment_service, UsersRepo())
#     payment_service.users_service = users_service
    
#     return users_service

# async def get_payment_service() -> "PaymentService":
#     from api.internal.services.users import UsersService
#     from api.internal.services.payment import PaymentService
    
#     users_service = UsersService(None, UsersRepo())
#     payment_service = PaymentService(users_service, PaymentRepo())
#     users_service.payment_service = payment_service
    
#     return payment_service