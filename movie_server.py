from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("MovieMCP", log_level="ERROR")
movies = {
"O silencio2":"O filme relata sobre animais com audição sensível",
"Origem": "O filme relata a história de um mundo com looping infinito, com seres estranhos",
"As branquelas": "O filme relata a história de duas irmãs que se disfarçam de mulheres brancas para se infiltrar em uma festa de elite",
}
@mcp.tool(
    name="read_movie_contents",
    description="read the contents of a movie and return it as a string."
)
def read_movie(
    movie_id: str = Field(description="id of the movie to read")
    ):
    if movie_id not in movies:
        raise ValueError(f"Movie with id {movie_id} not found")
    return movies[movie_id] 
@mcp.tool(
    name="edit_movie",
    description="Edit a movie by replacing a string in the movie content with a new string."
)
def edit_movie(
    movie_id: str = Field(description="Id of the movie that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if movie_id not in movies:
        raise ValueError(f"Movie with id {movie_id} not found")
    
    movies[movie_id] = movies[movie_id].replace(old_str, new_str)


