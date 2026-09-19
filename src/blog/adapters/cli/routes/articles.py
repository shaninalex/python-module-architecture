import click
from blog.bootstrap.app import Application
from blog.bootstrap.cli import async_cli_command
from blog.modules import content


@click.group("articles")
def articles_group() -> None:
    """Articles management."""


@articles_group.command("publish")
@click.argument("article_id", type=int)
@async_cli_command
async def publish_article(app: Application, article_id: int) -> int:
    """Publish article by ID."""
    view = await app.core.commands.execute(
        content.PublishArticle(article_id=article_id)
    )
    click.secho(f"Successfully published: '{view.title}' (slug: {view.slug})", fg="green")
    return 0


@articles_group.command("list")
@click.option("--limit", default=10, type=int)
@async_cli_command
async def list_articles(app: Application, limit: int) -> int:
    """Get list of recent articles."""
    page = await app.core.queries.ask(
        content.ListArticles(tag=None, author_id=None, offset=0, limit=limit)
    )
    for item in page.items:
        click.echo(f"[{item.id}] {item.title} by {item.author_name}")
    return 0
