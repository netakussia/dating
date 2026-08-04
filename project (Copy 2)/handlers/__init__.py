from handlers import admin, appeals, common, confessions, dating, likes, profile, registration

routers = (common.router, registration.router, profile.router, dating.router, likes.router, confessions.router, appeals.router, admin.router)
