from app import app
from flask import jsonify,request
from models import User,Post,Comment
from app import app, db
from werkzeug.exceptions import BadRequest,NotFound
from flask_jwt_extended import get_jwt_identity,jwt_required

@app.route('/',methods=['GET'])
def home():
    return jsonify(message="Hello world!")
@app.route("/V1/register",methods=["POST"])
def register():
    data=request.get_json()
    if not data:
        return {"message":"invalid data!"},400
    email=data.get("email")
    username = data.get("username")
    password = data.get("password")
    if not email or not username or not password:
        return{"message":"missing field"},400
    user= User(email=email,username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="user registered successfully!"),201
@app.route("/V1/login",methods=["POST"])
def login():
    data=request.get_json()
    if not data:
        raise BadRequest("INVALID DATA")
    email = data.get("email")
    password = data.get("password")
    token, _ =User.authenticate(email,password)
    if not token:
        raise BadRequest("INVALID CREDENTIALS!")
    return jsonify(access_token =token),200
@app.route("/V1/posts",methods=["POST"])
@jwt_required()
def add_post():
    user_id=int(get_jwt_identity())
    data=request.get_json()
    title = data.get("title")
    body = data.get("body")
    if not title or not body:
        raise BadRequest("missing field!")
    post= Post(title=title,body=body,author_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify(message="post added successfully!")

@app.route("/V1/posts",methods=["GET"])
def get_posts():
    posts=Post.query.all()
    return jsonify(posts=[p.to_dic() for p in posts]),200
@app.route("/V1/post/<int:post_id>",methods=["GET"])
def get_post(post_id):
    post=Post.query.get(post_id)
    if not post:
        raise NotFound("post not  found")
    return jsonify(posts=post.to_dic()),200

@app.route("/V1/post/<int:post_id>",methods=["PATCH"])
@jwt_required()
def update_post(post_id):
    user_id=int(get_jwt_identity())
    post=Post.query.get(post_id)
    if not post:
        raise NotFound("post not found!")
    if user_id!=post_id:
        raise BadRequest("permission denied!")
    data=request.get_json()
    post.title=data.get("title",post.title)
    post.body=data.get("body",post.body)
    db.session.commit()
    return jsonify(message="post added successfully!"),200


@app.route("/V1/post/<int:post_id>",methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id=int(get_jwt_identity())
    post=Post.query.get(post_id)
    if not post:
        raise NotFound("post not found!")
    if user_id != post_id:
        raise BadRequest("permission denied!")
    db.session.delete(post)
    db.session.commit()
    return jsonify(message="post deleted successfully!"),200

@app.route("/V1/post/<int:post_id>/comment",methods=["POST"])
@jwt_required()
def add_comment(post_id):
    user_id=int(get_jwt_identity())
    post=Post.query.get(post_id)
    if not post:
        raise NotFound("post not found!")
    data=request.get_json()
    body=data.get("body")
    if not body:
        raise BadRequest("missing data")
    comment=Comment(body=body,author_id=user_id,post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(message="comment added successfully!"),200


@app.route("/V1/post/<int:post_id>/comment",methods=["GET"])
def get_comment(post_id):
    post=Post.query.get(post_id)
    if not post:
        raise NotFound("post not found!")
    comments=post.comments.all()
    return jsonify([c.to_dic() for c in comments])







