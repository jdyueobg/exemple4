class Post:
    def __init__(self, id, photo_url, name, body):
        self.id = id
        self.photo_url = photo_url
        self.name = name
        self.body = body

class PostStore:
    def __init__(self):
        self.posts = []

    def add(self, post):
        self.posts.append(post)

    def get_all(self):
        return self.posts

    def delete(self, post_id):
        self.posts = [post for post in self.posts if post.id != post_id]