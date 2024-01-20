from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app)

connection = psycopg.connect(
    host='localhost',
    dbname='taskdata',
    user='postgres',
    password='password',
)


@app.route('/tododata', methods=['GET'])
def get_task():
    sql = '''
    SELECT *
    FROM タスク;
    '''
    result = connection.execute(sql)
    publishers = []
    for row in result:
        publishers.append({'id': row[0], 'text': row[1], 'date':row[2], 'status':row[3]})
    return jsonify(publishers)


@app.route('/tododata/create', methods=['POST'])
def post_task():

    sql = '''
    SELECT タスクID
    FROM タスク;
    '''
    result = connection.execute(sql)
    key = []
    for row in result:
        key.append(row[0])
    new_key = 1
    while True:
        if new_key not in key:
            break
        new_key += 1
    content = request.get_json()
    
    try:
        sql = '''
        INSERT INTO タスク (タスクID, タスク内容, 日時, ステータス)
        VALUES
        (%(todo_id)s, %(todo_text)s, %(todo_date)s, %(todo_status)s);
        '''
        connection.execute(sql,{'todo_id': new_key, 'todo_text': content["text"], 'todo_date': content["date"], 'todo_status': content["status"]})
    except Exception:
        connection.rollback()
    else:
        connection.commit()
    
    try:
        sql = '''
        INSERT INTO タスクデータ (タスクID, ユーザーID)
        VALUES
        (%(task_id)s,%(user_id)s);
        '''
        connection.execute(sql,{'task_id': new_key, 'user_id': content["userID"]})
    except Exception:
        connection.rollback()
    else:
        connection.commit()

    
    return jsonify({'message': 'created'})

@app.route('/tododata/update', methods=['POST'])
def update_task():
    content = request.get_json()
    print(content)
    try:
        sql = '''
        UPDATE タスク SET ステータス = %(todo_status)s WHERE タスクID = %(todo_id)s;
        '''
        connection.execute(sql,{'todo_status': content["status"], 'todo_id': content["id"]})
    except Exception:
        connection.rollback()
    else:
        connection.commit()
    
    return jsonify({'message': 'updated'})

@app.route('/tododata/delete/<int:id>', methods=['POST'])
def delete_task(id):
    try:
        sql = '''
        DELETE FROM タスクデータ WHERE タスクID = %(todo_id)s
        '''
        connection.execute(sql,{'todo_id': id})
    except Exception:
        connection.rollback()
    else:
        connection.commit()
    
    return jsonify({'message': 'created'})

@app.route('/user', methods=['GET'])
def get_user():
    sql = '''
    SELECT *
    FROM ユーザー;
    '''
    result = connection.execute(sql)
    user = []
    for row in result:
        user.append({'userID': row[0], 'userName': row[1], 'userPassword':row[2]})
    return jsonify(user)

@app.route('/user/create', methods=['POST'])
def post_user():
    content = request.get_json()
    
    try:
        sql = '''
        INSERT INTO ユーザー (ユーザーID, 名前, パスワード)
        VALUES
        (%(user_id)s, %(user_name)s, %(user_password)s);
        '''
        connection.execute(sql,{'user_id': content["userID"], 'user_name': content["userName"], 'user_password': content["userPassword"]})
    except Exception:
        connection.rollback()
    else:
        connection.commit()

    
    return jsonify({'message': 'created'})

@app.route('/taskdata',methods=['POST'])
def get_taskdata():
    content = request.get_json()
    sql = '''
    SELECT タスク.タスクID, タスク内容, 日時, ステータス 
    FROM タスク JOIN タスクデータ ON タスク.タスクID = タスクデータ.タスクID 
    WHERE ユーザーID = %(user_id)s;
    '''
    result = connection.execute(sql,{'user_id': content["userID"]})
    publishers = []
    for row in result:
        publishers.append({'id': row[0], 'text': row[1], 'date':row[2], 'status':row[3]})
    return jsonify(publishers)