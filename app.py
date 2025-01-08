import os
import random
import socket
from datetime import datetime
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# 获取 MySQL 配置
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_USER = os.getenv('MYSQL_USER', 'soniq')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DB = os.getenv('MYSQL_DB', 'music_db')

# 数据库连接
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# 获取每日歌曲
@app.route('/api/daily_song', methods=['GET'])
def daily_song():
    today_date = datetime.now().date()

    # 检查是否已有每日歌曲
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT song_id FROM daily_song WHERE date = %s", (today_date,))
    result = cursor.fetchone()

    if not result:
        # 如果没有每日歌曲记录，随机选择一首歌曲
        cursor.execute("SELECT id FROM songs ORDER BY RAND() LIMIT 1")
        song = cursor.fetchone()
        song_id = song['id']
        
        # 将选中的歌曲 ID 和日期保存到数据库
        cursor.execute("INSERT INTO daily_song (date, song_id) VALUES (%s, %s)", (today_date, song_id))
        connection.commit()

    else:
        song_id = result['song_id']

    # 获取歌曲详细信息
    cursor.execute("SELECT * FROM songs WHERE id = %s", (song_id,))
    song = cursor.fetchone()
    cursor.close()
    connection.close()

    # 构建歌曲的 URL
    audio_url = song['file_path']
    return jsonify({
        'title': song['title'],
        'audio_url': audio_url
    })

# 获取主机信息
@app.route('/api/host_info', methods=['GET'])
def host_info():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return jsonify({'host_name': host_name, 'host_ip': host_ip})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
