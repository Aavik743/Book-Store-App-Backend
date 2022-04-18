from .apis import Register_API, Verification_API, Login_API, Reset_Password_API

user_routes = [
    (Register_API, '/register'),
    (Verification_API, '/verification'),
    (Login_API, '/login'),
    (Reset_Password_API, '/resetpassword')
]
