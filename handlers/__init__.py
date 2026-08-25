from handlers import (
    admin,
    appeals,
    callback_fallback,
    common,
    confessions,
    dating,
    likes,
    profile,
    registration,
    verification,
)

routers = (
    common.router,
    registration.router,
    profile.router,
    verification.router,
    dating.router,
    likes.router,
    confessions.router,
    appeals.router,
    admin.router,
    callback_fallback.router,
)
