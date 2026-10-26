def meta_description(text):
    """Text for a page's meta description: one line, at most 160 characters."""
    return ' '.join(text.split())[:160]
