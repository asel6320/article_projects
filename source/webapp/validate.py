def article_validate(article):
    errors = {}
    if not article.title:
        errors['title'] = "Title is required"
    elif len(article.title) < 50:
        errors['title'] = "Title is too short"

    if not article.content:  # you can add regular expressions
        errors['content'] = "Content is required"

    if not article.author:
        errors['author'] = "Author is required"

    return errors

