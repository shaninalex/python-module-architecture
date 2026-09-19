from blog.core import errors
from blog.core.actor import Actor

ROLE_ACTIONS: dict[str, frozenset[str]] = {
    "reader": frozenset({"comment.post"}),
    "author": frozenset({"comment.post", "article.draft", "article.publish"}),
    "editor": frozenset({"comment.post", "comment.moderate", "article.draft", "article.publish"}),
    "admin": frozenset({"*"}),
}


class Guard:
    def check(self, actor: Actor, action: str) -> None:
        for role in actor.roles:
            allowed = ROLE_ACTIONS.get(role, frozenset())
            if "*" in allowed or action in allowed:
                return
        raise errors.forbidden("auth.forbidden", "You are not allowed to do this.")
