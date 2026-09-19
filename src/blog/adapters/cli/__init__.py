import click
from blog.adapters.cli.routes.articles import articles_group


@click.group()
@click.option(
    "-c", "--config",
    "config_path",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Path to YAML configuration file.",
)
@click.pass_context
def cli_root(ctx: click.Context, config_path: str | None) -> None:
    """Application entry point."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path


cli_root.add_command(articles_group)
