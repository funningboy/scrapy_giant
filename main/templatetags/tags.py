from main.forms import FormSearchItem, FormPortfolioItem

def default_tags(**kwargs):
    tags = {
        'searchform': FormSearchItem(),
        'portfolioform': FormPortfolioItem()
    }
    return tags

def home_tags(**kwargs):
    return default_tags(**kwargs)

def about_tags(**kwargs):
    return default_tags(**kwargs)
