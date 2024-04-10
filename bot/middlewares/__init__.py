from bot.dispatcher import dp
from .discrimin_filter import DiscriminationMiddleware
from .throttling import ThrottlingMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(DiscriminationMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())