from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app)

connection = psycopg.connect(
    host='localhost',
    dbname='tododata',
    user='postgres',
    password='password',
)


@app.route('/tododata', methods=['GET'])
def get_publishers():
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
def post_publisher():

    sql = '''
    SELECT ID
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
        INSERT INTO タスク (ID, タスク内容, 日時, ステータス)
        VALUES
        (%(todo_id)s, %(todo_text)s, %(todo_date)s, %(todo_status)s);
        '''
        connection.execute(sql,{'todo_id': new_key, 'todo_text': content["text"], 'todo_date': content["date"], 'todo_status': content["status"]})
    except Exception:
        connection.rollback()
    else:
        connection.commit()

    
    return jsonify({'message': 'created'})

@app.route('/tododata/update', methods=['POST'])
def update_tododata():
    content = request.get_json()
    print(content)
    try:
        sql = '''
        UPDATE タスク SET ステータス = %(todo_status)s WHERE ID = %(todo_id)s;
        '''
        connection.execute(sql,{'todo_status': content["status"], 'todo_id': content["id"]})
    except Exception:
        connection.rollback()
    else:
        connection.commit()
    
    return jsonify({'message': 'updated'})

@app.route('/tododata/delete/<int:id>', methods=['POST'])
def delete_tododata(id):
    try:
        sql = '''
        DELETE FROM タスク WHERE ID = %(todo_id)s
        '''
        connection.execute(sql,{'todo_id': id})
    except Exception:
        connection.rollback()
    else:
        connection.commit()
    
    return jsonify({'message': 'created'})