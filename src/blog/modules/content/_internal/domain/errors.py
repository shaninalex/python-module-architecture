from blog.core.errors import conflict, not_found, validation

EMPTY_TITLE = validation("content.empty_title", "Title must not be empty.")
EMPTY_BODY = validation("content.empty_body", "Cannot publish an article with no body.")
SLUG_TAKEN = conflict("content.slug_taken", "An article with this slug already exists.")
ALREADY_PUBLISHED = conflict("content.already_published", "Article is already published.")
NOT_PUBLISHED = conflict("content.not_published", "Only a published article can be hidden.")
NO_SUCH_ARTICLE = not_found("content.no_such_article", "Article not found.")