# === API CONNECTION ===

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection succesfull!")
        break
    except Exception as error:
        print("Database connection FAILED!")
        print("Error: ", error)
        time.sleep(10)

# === API WITH SQL===

@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts

@router.get("/posts/{id}", response_model= schemas.PostResponse)
def get_posts_by_id(id: str, response: Response):
    cursor.execute("""SELECT *
                   FROM posts
                   WHERE id = %s""",
                   (str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def post_posts(payload: schemas.Post):
    cursor.execute("""INSERT INTO posts (title, content, published)
                   VALUES (%s, %s, %s) 
                   RETURNING *""",
                   (payload.title, payload.content, payload.published))
    posts = cursor.fetchone()

    conn.commit()

    return posts

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts
                   WHERE id = %s 
                   returning *""",
                   (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model= schemas.PostResponse)
def update_posts(id: int, payload: schemas.Post):
    cursor.execute("""UPDATE posts 
                   SET title = %s, content = %s, published = %s 
                   WHERE id = %s
                   RETURNING *""",
                   (payload.title, payload.content, payload.published, str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post
