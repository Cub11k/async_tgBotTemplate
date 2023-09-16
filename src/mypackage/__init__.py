import asyncio
import os

from .bot import setup_bot, launch_bot
from .cli import define_arg_parser
from .config import load_config
from .logger import setup_logger
from .webhook import setup_app, Application

if os.environ.get('USE_UVLOOP'):
    uvloop_installed = True
    try:
        import uvloop
    except ImportError:
        uvloop = None
        uvloop_installed = False

    if uvloop_installed and uvloop is not None:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    else:
        raise RuntimeError('You\'re trying to use uvloop, but it\'s not installed. '
                           'Please install it first: pip install uvloop')


async def _webhook_app() -> Application:
    # this function is just an example of how you can create the app factory
    config_path = os.environ.get('CONFIG_PATH', 'config.toml')
    use_env_vars = bool(os.environ.get('CONFIG_USE_ENV_VARS', False))
    config_env_mapping_path = os.environ.get('CONFIG_ENV_MAPPING_PATH', 'config_env_mapping.toml')
    cfg = load_config(config_path, use_env_vars, config_env_mapping_path)

    bot_logger = setup_logger(cfg.bot.logger)
    bot_ = setup_bot(cfg.bot, cfg.messages, cfg.buttons, bot_logger)

    app = setup_app(cfg.bot.webhook.path)
    app.ctx.bot = bot_
    app.ctx.secret_token = cfg.bot.webhook.secret_token
    app.ctx.logger = setup_logger(cfg.logger)

    # use_webhook is intentionally hard-coded to True here as we're using webhook
    await launch_bot(bot_, cfg.bot.drop_pending, True, cfg.bot.allowed_updates, cfg.bot.webhook)
    return app


def webhook_app() -> Application:
    return asyncio.run(_webhook_app())


async def _main():
    # If you wish to use webhook, you'll probably want to launch the bot using the web-server, e.g. gunicorn
    # In this case you should be calling the webhook_app_factory function
    arg_parser = define_arg_parser()
    args = arg_parser.parse_args()
    cfg = load_config(args.config_path, args.use_env_vars, args.config_env_mapping_path)
    bot_logger = setup_logger(cfg.bot.logger)
    bot_ = setup_bot(cfg.bot, cfg.messages, cfg.buttons, bot_logger)
    # use_webhook is intentionally hard-coded to False here as we're using long polling
    await launch_bot(bot_, cfg.bot.drop_pending, False, cfg.bot.allowed_updates, cfg.bot.webhook)


# Sync main wrapper
def main():
    asyncio.run(_main())
