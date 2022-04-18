from .apis import Register_API, Verification_API

user_routes = [
    (Register_API, '/register'),
    (Verification_API, '/verification')
]
