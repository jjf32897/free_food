from facepy import GraphAPI

graph = GraphAPI(access_token)

print graph.get('me/posts')
