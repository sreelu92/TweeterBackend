import mariadb
from flask import Flask,request,Response
import json
import dbcreds
from flask_cors import CORS
import secrets

app= Flask(__name__)
CORS(app)

@app.route('/api/users',methods=['GET','POST','PATCH','DELETE'])
def users():
    if request.method=='GET':
        conn=None
        cursor=None
        tweet_userid=request.args.get("userId")
        tweets=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()   
            if tweet_userid:
                cursor.execute("SELECT * FROM users WHERE id=?",[tweet_userid])
                tweets=cursor.fetchall()
                for tweet in tweets:
                    tweet[0],tweet[1],tweet[2],tweet[3],tweet[4],tweet[5]
                    tweetdata={"userId":tweet[0],"email":tweet[1],"bio":tweet[3],"birthdate":tweet[4],"username":tweet[5]}
            else:
                cursor.execute("SELECT * FROM users")
                tweets=cursor.fetchall()
                tweetdata=[]

                for tweet in tweets:
                    tweet[0],tweet[1],tweet[2],tweet[3],tweet[4],tweet[5]
                    tweetdata.append({"userId":tweet[0],"email":tweet[1],"bio":tweet[3],"birthdate":tweet[4],"username":tweet[5]})
        
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweets!=None):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='POST':
        conn=None
        cursor=None
        tweet_email=request.json.get("email")
        tweet_username=request.json.get("username")
        tweet_password=request.json.get("password")
        tweet_bio=request.json.get("bio")
        tweet_birthdate=request.json.get("birthdate")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            randomtokens=secrets.token_hex(10)
            if randomtokens:
                cursor.execute("INSERT INTO users(email,password,bio,birthday,username) VALUES(?,?,?,?,?)",[tweet_email,tweet_password,tweet_bio,tweet_birthdate,tweet_username,])
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?",[tweet_username,tweet_password])
                tweets=cursor.fetchall()
                for tweet in tweets:
                    tweet[0]
                cursor.execute("INSERT INTO user_session(user_id,login_token) VALUES(?,?)",[tweet[0],randomtokens,])
                tweetdata={"email":tweet_email,"userId":tweet[0],"bio":tweet_bio,"birthdate":tweet_birthdate,"username":tweet_username,"loginToken":randomtokens}
                conn.commit()
                rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='PATCH':
        conn=None
        cursor=None
        tweet_email=request.json.get("email")
        tweet_username=request.json.get("username")
        tweet_password=request.json.get("password")
        tweet_bio=request.json.get("bio")
        tweet_birthdate=request.json.get("birthdate")
        tweet_logintoken=request.json.get("loginToken")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if tweet_logintoken:
                if tweet_email!="" and tweet_email!=None:
                    cursor.execute("UPDATE users INNER JOIN user_session ON users.id=user_session.user_id SET email=? WHERE login_Token=?",[tweet_email,tweet_logintoken])
                if tweet_username!="" and tweet_username!=None:
                    cursor.execute("UPDATE users INNER JOIN user_session ON users.id=user_session.user_id SET username=? WHERE login_Token=?",[tweet_username,tweet_logintoken])
                if tweet_password!="" and tweet_password!=None:
                    cursor.execute("UPDATE users INNER JOIN user_session ON users.id=user_session.user_id SET password=? WHERE login_Token=?",[tweet_password,tweet_logintoken])
                if tweet_bio!="" and tweet_bio!=None:
                    cursor.execute("UPDATE users INNER JOIN user_session ON users.id=user_session.user_id SET bio=? WHERE login_Token=?",[tweet_bio,tweet_logintoken])
                if tweet_birthdate!="" and tweet_birthdate!=None:
                    cursor.execute("UPDATE users INNER JOIN user_session ON users.id=user_session.user_id SET birthday=? WHERE login_Token=?",[tweet_birthdate,tweet_logintoken])

                conn.commit()
                rows=cursor.rowcount
                cursor.execute("SELECT u.username,u.email,u.bio,u.birthday,us.user_id FROM users u INNER JOIN user_session us ON u.id=us.user_id WHERE us.login_token=?",[tweet_logintoken])
                infos=cursor.fetchall()
                for info in infos:
                    info[0],info[1],info[2],info[3],info[4]
                    tweetdata={"username":info[0],"email":info[1],"bio":info[2],"birthdate":info[3],"userId":info[4]}
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Updated failed",mimetype="text/html",status=500)
    

    
    elif request.method=='DELETE':
        conn=None
        cursor=None
        rows=None
        tweet_password=request.json.get("password")
        tweet_logintoken=request.json.get("loginToken")
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if tweet_logintoken:
                cursor.execute("SELECT u.password FROM users u INNER JOIN user_session us ON u.id=us.user_id WHERE us.login_token=?",[tweet_logintoken])
                users=cursor.fetchall()
                for user in users:
                    user[0]
                if (user[0]==tweet_password):
                    cursor.execute("DELETE users,user_session FROM users INNER JOIN user_session ON users.id=user_session.user_id WHERE password=? AND login_token=?",[tweet_password,tweet_logintoken])
                    conn.commit()
                    rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(users!=None):
                return Response("Delete success!",mimetype="text/html",status=204)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)

@app.route('/api/login',methods=['POST','DELETE'])
def login():
    if request.method=='POST':
        conn=None
        cursor=None
        tweet_email=request.json.get("email")
        tweet_password=request.json.get("password")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            randomtokens=secrets.token_hex(10)   
            if randomtokens:
                cursor.execute("SELECT * FROM users WHERE email=? AND password=?",[tweet_email,tweet_password])
                tweets=cursor.fetchall()
                for tweet in tweets:
                    tweet[0]
                    tweet[1]
                    tweet[3]
                    tweet[4]
                    tweet[5]
                cursor.execute("INSERT INTO user_session(user_id,login_token) VALUES(?,?)",[tweet[0],randomtokens,])
                tweetdata={"userId":tweet[0],"email":tweet[1],"bio":tweet[3],"birthday":tweet[4],"username":tweet[5],"loginToken":randomtokens}
                conn.commit()
                rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='DELETE':
        conn=None
        cursor=None
        rows=None
        tweet_logintoken=request.json.get("loginToken")
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if tweet_logintoken:
                cursor.execute("SELECT u.id FROM users u INNER JOIN user_session us ON u.id=us.user_id WHERE us.login_token=?",[tweet_logintoken])
                users=cursor.fetchall()
                for user in users:
                    user[0]
                if user[0]:
                    cursor.execute("DELETE user_session FROM users INNER JOIN user_session ON users.id=user_session.user_id WHERE login_token=?",[tweet_logintoken])
                    conn.commit()
                    rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Delete success!",mimetype="text/html",status=204)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)

@app.route('/api/tweets',methods=['POST','PATCH','GET','DELETE'])
def tweets():
    if request.method=='POST':
        conn=None
        cursor=None
        tweet_content=request.json.get("content")
        tweet_logintoken=request.json.get("loginToken")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if tweet_logintoken:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[tweet_logintoken])
                users=cursor.fetchall()
                for user in users:
                    user[1]
                cursor.execute("INSERT INTO tweet(content,user_id) VALUES(?,?)",[tweet_content,user[1]])
                cursor.execute("SELECT u.username,t.content,t.created_at,t.user_id FROM users u INNER JOIN tweet t ON u.id=t.user_id WHERE t.user_id=?",[user[1]])
                infos=cursor.fetchall()
                for info in infos:
                    info[0],info[1],info[2],info[3]
                    tweetdata={"username":info[0],"content":info[1],"created_at":info[2],"userId":info[3]}
                conn.commit()
                rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(users!=None):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='GET':
        conn=None
        cursor=None
        tweet_userid=request.args.get("userId")
        tweetts=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()   
            if tweet_userid:
                cursor.execute("SELECT * FROM tweet WHERE user_id=?",[tweet_userid])
                tweetts=cursor.fetchall()
                tweetarray=[]
                for tweett in tweetts:
                    tweett[0]
                    tweett[1]
                    tweett[2]
                    tweett[3]
                    tweetarray.append({"tweetId":tweett[0],"content":tweett[1],"created_at":tweett[2],"userId":tweett[3]}) 
            else:
                cursor.execute("SELECT t.content,t.created_at,t.id,u.username FROM tweet t INNER JOIN users u ON u.id=t.user_id")
                tweetts=cursor.fetchall()
                tweetarray=[]
                for tweett in tweetts:
                    tweett[0]
                    tweett[1]
                    tweett[2]
                    tweett[3]
                    tweetarray.append({"content":tweett[0],"created_at":tweett[1],"tweetId":tweett[2],"username":tweett[3]})
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetts!=None):
                return Response(json.dumps(tweetarray,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='PATCH':
        conn=None
        cursor=None
        tweet_id=request.json.get("tweetId")
        tweet_logintoken=request.json.get("loginToken")
        tweet_content=request.json.get("content")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if tweet_logintoken:
                if tweet_content!="" and tweet_content!=None:
                    cursor.execute("UPDATE tweet SET content=? WHERE id=?",[tweet_content,tweet_id])
            conn.commit()
            rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Updated success!",mimetype="text/html",status=204)
            else:
                return Response("Updated failed",mimetype="text/html",status=500)
    


    elif request.method=='DELETE':
        conn=None
        cursor=None
        rows=None
        tweet_logintoken=request.json.get("loginToken")
        tweet_id=request.json.get("tweetId")
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if tweet_logintoken:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[tweet_logintoken])
                users=cursor.fetchall()
                for user in users:
                    user[1]
                cursor.execute("SELECT * FROM tweet WHERE id=?",[tweet_id])
                newids=cursor.fetchall()
                for newid in newids:
                    newid[3]
                if(user[1]==newid[3]):
                    cursor.execute("DELETE tweet FROM tweet WHERE id=?",[tweet_id,])
                    conn.commit()
                    rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Delete success!",mimetype="text/html",status=204)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)

@app.route('/api/comments',methods=['POST','PATCH','GET','DELETE'])
def comments():
    if request.method=='POST':
        conn=None
        cursor=None
        comment_content=request.json.get("content")
        comment_logintoken=request.json.get("loginToken")
        tweet_id=request.json.get("tweetId")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if comment_logintoken:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[comment_logintoken])
                users=cursor.fetchall()
                for user in users:
                    user[1]
                cursor.execute("INSERT INTO comment(content,user_id,tweet_id) VALUES(?,?,?)",[comment_content,user[1],tweet_id])
                conn.commit()
                rows=cursor.rowcount
                cursor.execute("SELECT u.username,c.content,c.created_at,c.user_id,c.tweet_id,c.id FROM users u INNER JOIN comment c ON u.id=c.user_id WHERE c.tweet_id=?",[tweet_id])
                infos=cursor.fetchall()
                tweetdata=[]
                for info in infos:
                    info[0],info[1],info[2],info[3],info[4],info[5]
                    tweetdata.append({"username":info[0],"content":info[1],"created_at":info[2],"userId":info[3],"tweetId":info[4],"commentId":info[5]})
           
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(infos!=None):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='GET':
        conn=None
        cursor=None
        tweet_id=request.args.get("tweetId")
        tweetts=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()   
            if tweet_id:
                cursor.execute("SELECT * FROM comment WHERE tweet_id=?",[tweet_id])
                tweetts=cursor.fetchall()
                tweetarray=[]
                for tweett in tweetts:
                    tweett[0]
                    tweett[1]
                    tweett[2]
                    tweett[3]
                    tweett[4]
                    tweetarray.append({"userId":tweett[0],"tweetId":tweett[1],"commentId":tweett[2],"content":tweett[3],"created_at":tweett[4]})
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")        
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetts!=None):
                return Response(json.dumps(tweetarray,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='PATCH':
        conn=None
        cursor=None
        comment_id=request.json.get("commentId")
        comment_logintoken=request.json.get("loginToken")
        comment_content=request.json.get("content")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if comment_logintoken:
                if comment_content!="" and comment_content!=None:
                    cursor.execute("UPDATE comment SET content=? WHERE id=?",[comment_content,comment_id])
                    conn.commit()
                    rows=cursor.rowcount
                    cursor.execute("SELECT c.user_id,c.tweet_id,c.id,c.content,c.created_at,u.username FROM comment c INNER JOIN users u ON u.id=c.user_id WHERE c.id=?",[comment_id])
                    infos=cursor.fetchall()
                    for info in infos:
                        info[0],info[1],info[2],info[3],info[4],info[5]
                        commentdata={"userId":info[0],"tweetId":info[1],"commentId":info[2],"content":info[3],"created_at":info[4],"username":info[5]}
               
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response(json.dumps(commentdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Updated failed",mimetype="text/html",status=500)

    elif request.method=='DELETE':
        conn=None
        cursor=None
        rows=None
        comment_id=request.json.get("commentId")
        comment_logintoken=request.json.get("loginToken")


        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if comment_logintoken:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[comment_logintoken])
                users=cursor.fetchall()
                for user in users:
                    user[1]
                cursor.execute("SELECT * FROM comment WHERE id=?",[comment_id])
                newids=cursor.fetchall()
                for newid in newids:
                    newid[0]
                if(user[1]==newid[0]):
                    cursor.execute("DELETE comment FROM comment WHERE id=?",[comment_id,])
                    conn.commit()
                    rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Delete success!",mimetype="text/html",status=204)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)

@app.route('/api/tweetlikes',methods=['POST','GET','DELETE'])
def tweet_likes():
    if request.method=='POST':
        conn=None
        cursor=None
        tweet_logintoken=request.json.get("loginToken")
        tweet_id=request.json.get("tweetId")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if tweet_logintoken:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[tweet_logintoken])
                users=cursor.fetchall()
                for user in users:
                    user[1]

                cursor.execute("INSERT INTO tweet_like(user_id,tweet_id) VALUES(?,?)",[user[1],tweet_id])
                conn.commit()
                rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("OK",mimetype="text/html",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='GET':
        conn=None
        cursor=None
        tweet_id=request.args.get("tweetId")
        tweetts=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()   
            if tweet_id:
                cursor.execute("SELECT tl.user_id,tl.tweet_id,u.username FROM tweet_like tl INNER JOIN users u ON u.id=tl.user_id WHERE tweet_id=?",[tweet_id])
                tweetts=cursor.fetchall()
                tweetarray=[]
                for tweett in tweetts:
                    tweett[0]
                    tweett[1]
                    tweett[2]
                    tweetarray.append({"userId":tweett[0],"tweetId":tweett[1],"username":tweett[2]})
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetts!=None):
                return Response(json.dumps(tweetarray,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='DELETE':
        conn=None
        cursor=None
        rows=None
        token=request.json.get("loginToken")
        tweetid=request.json.get("tweetId")
        
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if token:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[token])
                tweetdata=cursor.fetchall()
                for twee in tweetdata:
                    twee[1]
                cursor.execute("SELECT * FROM tweet WHERE id=?",[tweetid])
                users=cursor.fetchall()
                for user in users:
                    user[3]
                if(twee[1]==user[3]):
                    cursor.execute("DELETE tweet_like FROM tweet_like WHERE user_id=? AND tweet_id=?",[twee[1],tweetid])
                    conn.commit()
                    rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetdata!=None):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)


@app.route('/api/commentlikes',methods=['POST','GET','DELETE'])
def comment_likes():
    if request.method=='POST':
        conn=None
        cursor=None
        token=request.json.get("loginToken")
        commentid=request.json.get("commentId")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if token:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[token])
                users=cursor.fetchall()
                for user in users:
                    user[1]

                cursor.execute("INSERT INTO comment_like(user_id,comment_id) VALUES(?,?)",[user[1],commentid])
                conn.commit()
                rows=cursor.rowcount
                cursor.execute("SELECT cl.user_id,cl.comment_id,u.username FROM users u INNER JOIN comment_like cl ON u.id=cl.user_id WHERE comment_id=?",[commentid])
                comments=cursor.fetchall()
                for comment in comments:
                    comment[0],comment[1],comment[2]
                    commentdata={"userId":comment[0],"commentId":comment[1],"username":comment[2]}
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response(json.dumps(commentdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='GET':
        conn=None
        cursor=None
        commentid=request.args.get("commentId")
        tweetts=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()   
            if commentid:
                cursor.execute("SELECT cl.user_id,cl.comment_id,u.username FROM comment_like cl INNER JOIN users u ON u.id=cl.user_id WHERE comment_id=?",[commentid])
                tweetts=cursor.fetchall()
                tweetarray=[]
                for tweett in tweetts:
                    tweett[0]
                    tweett[1]
                    tweett[2]
                    tweetarray.append({"userId":tweett[0],"commentId":tweett[1],"username":tweett[2]})
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetts!=None):
                return Response(json.dumps(tweetarray,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='DELETE':
        conn=None
        cursor=None
        rows=None
        token=request.json.get("loginToken")
        commentid=request.json.get("commentId")
        
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if token:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[token])
                tweetdata=cursor.fetchall()
                for twee in tweetdata:
                    twee[1]
                cursor.execute("DELETE comment_like FROM comment_like WHERE user_id=? AND comment_id=?",[twee[1],commentid])
                conn.commit()
                rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetdata!=None):
                return Response(json.dumps(tweetdata,default=str),mimetype="application/json",status=200)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)

@app.route('/api/follows',methods=['POST','GET','DELETE'])
def createfollow():
    if request.method=='POST':
        conn=None
        cursor=None
        token=request.json.get("loginToken")
        followid=request.json.get("followId")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if token:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[token])
                users=cursor.fetchall()
                for user in users:
                    user[1]

                cursor.execute("INSERT INTO follow(user_id,follow_id) VALUES(?,?)",[user[1],followid])
                conn.commit()
                rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("followed",mimetype="text/html",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)
    
    elif request.method=='GET':
        conn=None
        cursor=None
        userid=request.args.get("userId")
        tweetts=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()   
            if userid:
                cursor.execute("SELECT u.id, u.email,u.bio,u.birthday,u.username FROM follow f INNER JOIN users u ON u.id=f.follow_id WHERE f.user_id=?",[userid])
                tweetts=cursor.fetchall()
                tweetarray=[]
                for tweett in tweetts:
                    tweett[0]
                    tweett[1]
                    tweett[2]
                    tweett[3]
                    tweett[4]
                    tweetarray.append({"userId":tweett[0],"email":tweett[1],"bio":tweett[2],"birthdate":tweett[3],"username":tweett[4]})
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetts!=None):
                return Response(json.dumps(tweetarray,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='DELETE':
        conn=None
        cursor=None
        rows=None
        token=request.json.get("loginToken")
        followid=request.json.get("followId")
        
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if token:
                cursor.execute("SELECT * FROM user_session WHERE login_token=?",[token])
                tweetdata=cursor.fetchall()
                for twee in tweetdata:
                    twee[1]
                cursor.execute("DELETE follow FROM follow WHERE user_id=? AND follow_id=?",[twee[1],followid])
                conn.commit()
                rows=cursor.rowcount
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Deleted",mimetype="text/html",status=200)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)

@app.route('/api/followers',methods=['GET'])
def getFollowers():
    if request.method=='GET':
        conn=None
        cursor=None
        userid=request.args.get("userId")
        tweetts=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()   
            if userid:
                cursor.execute("SELECT u.id, u.email,u.bio,u.birthday,u.username FROM follow f INNER JOIN users u ON u.id=f.user_id WHERE f.follow_id=?",[userid])
                tweetts=cursor.fetchall()
                tweetarray=[]
                for tweett in tweetts:
                    tweett[0]
                    tweett[1]
                    tweett[2]
                    tweett[3]
                    tweett[4]
                    tweetarray.append({"userId":tweett[0],"email":tweett[1],"bio":tweett[2],"birthdate":tweett[3],"username":tweett[4]})
        except mariadb.ProgrammingError as error:
            print("Something went wrong with coding ")
            print(error)
        except mariadb.DatabaseError as error:
            print("There is a database error")
            print(error)
        except mariadb.OperationalError as error:
            print("Connection error occured. Please try again later!")
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(tweetts!=None):
                return Response(json.dumps(tweetarray,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)






   


    


    

