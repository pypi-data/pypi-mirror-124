from animec import Anime, NoResultFound

def get_anime(name: str):
    
    try:
        anime = Anime(name)
        return anime
    except NoResultFound:
        return None

def iter_printable(target):
    if target and iter(target):
        return ", ".join(target)
    else:
        return target

def body(base: Anime):

    display_body = f"""
    
    Name: {base.name}
    Alt Titles: {base.alt_titles}
    
    Description: {base.description}
    
    Episodes: {base.episodes}
    Aired: {base.aired}
    Broadcast: {base.broadcast}
    Rating: {base.rating}
    Ranking: {base.ranked}
    Populatiry: {base.popularity}
    Type: {base.type}
    
    Status: {base.status}
    Producers: {iter_printable(base.producers)}
    Genres: {iter_printable(base.genres)}

    Opening Themes: {iter_printable(base.opening_themes)}
    Ending Themes: {iter_printable(base.ending_themes)}
    
    """

    return display_body

def prompt():

    inp = input("\nPlease input the name of the anime you wish to search for: ")
    anime = get_anime(inp)

    if anime:
        return body(anime)
    else:
        return "\nIt looks like I couldn't find the anime you were looking for."

print(prompt())
