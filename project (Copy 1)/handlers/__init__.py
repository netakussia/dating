from handlers import admin, common, confessions, dating, likes, profile, registration

routers = (common.router, registration.router, profile.router, dating.router, likes.router, confessions.router, admin.router)
