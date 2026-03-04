# -*- coding: utf-8 -*-
"""
SQLite数据库操作
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

from utils.config import DB_PATH


@dataclass
class Recording:
    id: str
    filename: str
    filepath: str
    duration: float
    file_size: int
    language: str
    created_at: str
    status: str  # pending, processing, completed, error
    keywords: str
    summary: str
    todos: str
    sentiment: str


@dataclass
class TranscriptSegment:
    id: int
    recording_id: str
    start_time: float
    end_time: float
    text: str
    speaker_id: str
    speaker_name: str
    is_highlighted: bool
    is_favorite: bool
    note: str


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        self._init_tables()
    
    def _init_tables(self):
        """初始化数据库表"""
        cursor = self.conn.cursor()
        
        # 录音文件表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recordings (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                duration REAL DEFAULT 0,
                file_size INTEGER DEFAULT 0,
                language TEXT DEFAULT 'zh',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                keywords TEXT,
                summary TEXT,
                todos TEXT,
                sentiment TEXT
            )
        """)
        
        # 转写内容表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recording_id TEXT,
                start_time REAL,
                end_time REAL,
                text TEXT,
                speaker_id TEXT,
                speaker_name TEXT,
                is_highlighted INTEGER DEFAULT 0,
                is_favorite INTEGER DEFAULT 0,
                note TEXT,
                FOREIGN KEY (recording_id) REFERENCES recordings(id)
            )
        """)
        
        # 说话人表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS speakers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recording_id TEXT,
                speaker_id TEXT,
                name TEXT,
                color TEXT,
                FOREIGN KEY (recording_id) REFERENCES recordings(id)
            )
        """)
        
        self.conn.commit()
    
    def add_recording(self, recording: Recording) -> bool:
        """添加录音记录"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO recordings 
                (id, filename, filepath, duration, file_size, language, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                recording.id, recording.filename, recording.filepath,
                recording.duration, recording.file_size, recording.language,
                recording.status
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"添加录音失败: {e}")
            return False
    
    def update_recording_status(self, recording_id: str, status: str):
        """更新录音状态"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE recordings SET status = ? WHERE id = ?",
            (status, recording_id)
        )
        self.conn.commit()
    
    def update_recording_analysis(self, recording_id: str, 
                                   keywords: list, summary: str, 
                                   todos: list, sentiment: dict):
        """更新分析结果"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE recordings 
            SET keywords = ?, summary = ?, todos = ?, sentiment = ?
            WHERE id = ?
        """, (
            json.dumps(keywords, ensure_ascii=False),
            summary,
            json.dumps(todos, ensure_ascii=False),
            json.dumps(sentiment, ensure_ascii=False),
            recording_id
        ))
        self.conn.commit()
    
    def add_transcript(self, recording_id: str, segments: List[Dict]):
        """添加转写内容"""
        cursor = self.conn.cursor()
        for seg in segments:
            cursor.execute("""
                INSERT INTO transcripts 
                (recording_id, start_time, end_time, text, speaker_id, speaker_name)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                recording_id,
                seg["start"],
                seg["end"],
                seg["text"],
                seg.get("speaker", "UNKNOWN"),
                seg.get("speaker", "说话人")
            ))
        self.conn.commit()
    
    def add_speakers(self, recording_id: str, speakers: List[Dict]):
        """添加说话人信息"""
        cursor = self.conn.cursor()
        for idx, spk in enumerate(speakers):
            cursor.execute("""
                INSERT INTO speakers (recording_id, speaker_id, name, color)
                VALUES (?, ?, ?, ?)
            """, (
                recording_id,
                spk["id"],
                spk.get("name", f"说话人{idx+1}"),
                spk.get("color", "#4ECDC4")
            ))
        self.conn.commit()
    
    def update_speaker_name(self, recording_id: str, speaker_id: str, new_name: str):
        """更新说话人名称"""
        cursor = self.conn.cursor()
        # 更新说话人表
        cursor.execute("""
            UPDATE speakers SET name = ? 
            WHERE recording_id = ? AND speaker_id = ?
        """, (new_name, recording_id, speaker_id))
        # 更新转写表
        cursor.execute("""
            UPDATE transcripts SET speaker_name = ?
            WHERE recording_id = ? AND speaker_id = ?
        """, (new_name, recording_id, speaker_id))
        self.conn.commit()
    
    def toggle_favorite(self, transcript_id: int) -> bool:
        """切换收藏状态"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT is_favorite FROM transcripts WHERE id = ?",
            (transcript_id,)
        )
        row = cursor.fetchone()
        if row:
            new_status = 0 if row["is_favorite"] else 1
            cursor.execute(
                "UPDATE transcripts SET is_favorite = ? WHERE id = ?",
                (new_status, transcript_id)
            )
            self.conn.commit()
            return bool(new_status)
        return False
    
    def toggle_highlight(self, transcript_id: int) -> bool:
        """切换高亮状态"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT is_highlighted FROM transcripts WHERE id = ?",
            (transcript_id,)
        )
        row = cursor.fetchone()
        if row:
            new_status = 0 if row["is_highlighted"] else 1
            cursor.execute(
                "UPDATE transcripts SET is_highlighted = ? WHERE id = ?",
                (new_status, transcript_id)
            )
            self.conn.commit()
            return bool(new_status)
        return False
    
    def add_note(self, transcript_id: int, note: str):
        """添加笔记"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE transcripts SET note = ? WHERE id = ?",
            (note, transcript_id)
        )
        self.conn.commit()
    
    def get_recordings(self) -> List[Recording]:
        """获取所有录音"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM recordings ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [Recording(**dict(row)) for row in rows]
    
    def get_transcripts(self, recording_id: str) -> List[TranscriptSegment]:
        """获取转写内容"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM transcripts 
            WHERE recording_id = ? 
            ORDER BY start_time
        """, (recording_id,))
        rows = cursor.fetchall()
        return [TranscriptSegment(**dict(row)) for row in rows]
    
    def get_speakers(self, recording_id: str) -> List[Dict]:
        """获取说话人列表"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM speakers WHERE recording_id = ?",
            (recording_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_favorites(self, recording_id: str) -> List[TranscriptSegment]:
        """获取收藏的内容"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM transcripts 
            WHERE recording_id = ? AND is_favorite = 1
            ORDER BY start_time
        """, (recording_id,))
        rows = cursor.fetchall()
        return [TranscriptSegment(**dict(row)) for row in rows]
    
    def delete_recording(self, recording_id: str):
        """删除录音及相关数据"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transcripts WHERE recording_id = ?", (recording_id,))
        cursor.execute("DELETE FROM speakers WHERE recording_id = ?", (recording_id,))
        cursor.execute("DELETE FROM recordings WHERE id = ?", (recording_id,))
        self.conn.commit()
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()
