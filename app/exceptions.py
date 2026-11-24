class ArticlesNotFoundError(Exception):
    """Raised when there is no Article found for the ticker in Qdrant"""
