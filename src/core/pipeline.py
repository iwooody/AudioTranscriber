# -*- coding: utf-8 -*-
"""
主处理流程
整合语音识别、说话人分离、NLP分析
"""

import uuid
from pathlib import Path
from typing import Callable, Dict
import librosa

from core.whisper_service import WhisperTranscriber
from core.speaker_diarization import SimpleSpeakerDiarizer
from core.nlp_summary import NLPSummarizer
from utils.database import Database, Recording


class TranscriptionPipeline:
    """转写处理流水线"""
    
    def __init__(self, model_name: str = "base"):
        """
        初始化流水线
        
        Args:
            model_name: Whisper模型名称
        """
        print("初始化处理流水线...")
        
        # 初始化各模块
        self.transcriber = WhisperTranscriber(model_name=model_name)
        self.diarizer = SimpleSpeakerDiarizer()
        self.nlp = NLPSummarizer()
        self.db = Database()
        
        print("流水线初始化完成")
    
    def process(self, audio_path: str, language: str = "zh",
                progress_callback: Callable = None) -> str:
        """
        处理音频文件
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码
            progress_callback: 进度回调函数，接收0-100的整数
            
        Returns:
            recording_id: 录音记录ID
        """
        # 生成唯一ID
        recording_id = str(uuid.uuid4())[:8]
        
        try:
            # 1. 获取音频信息
            print(f"\n{'='*50}")
            print(f"开始处理: {audio_path}")
            print(f"{'='*50}")
            
            duration = 0
            try:
                duration = librosa.get_duration(path=audio_path)
                print(f"音频时长: {duration/60:.1f}分钟")
            except:
                pass
            
            # 2. 添加到数据库
            recording = Recording(
                id=recording_id,
                filename=Path(audio_path).name,
                filepath=audio_path,
                duration=duration,
                file_size=Path(audio_path).stat().st_size,
                language=language,
                created_at="",
                status="processing",
                keywords="",
                summary="",
                todos="",
                sentiment=""
            )
            self.db.add_recording(recording)
            
            # 3. 语音识别
            if progress_callback:
                progress_callback(10, "正在识别语音...")
            
            # 根据时长选择处理方式
            if duration > 30 * 60:  # 超过30分钟
                result = self.transcriber.transcribe_long_audio(
                    audio_path, language,
                    progress_callback=lambda p: progress_callback(10 + int(p * 0.5))
                )
            else:
                result = self.transcriber.transcribe(
                    audio_path, language,
                    progress_callback=lambda p: progress_callback(10 + int(p * 0.5))
                )
            
            segments = result["segments"]
            full_text = result["full_text"]
            detected_language = result.get("language", language)
            
            print(f"识别完成，共 {len(segments)} 段")
            
            # 4. 说话人分离
            if progress_callback:
                progress_callback(60, "正在分离说话人...")
            
            segments = self.diarizer.diarize(audio_path, segments)
            
            # 获取说话人统计
            speaker_stats = self.diarizer.get_speaker_stats(segments)
            print(f"检测到 {len(speaker_stats)} 个说话人")
            
            # 5. NLP分析
            if progress_callback:
                progress_callback(80, "正在进行智能分析...")
            
            analysis = self.nlp.analyze_all(segments, full_text)
            
            print(f"关键词: {', '.join(analysis['keywords'][:5])}")
            print(f"待办事项: {len(analysis['todos'])}条")
            
            # 6. 保存到数据库
            if progress_callback:
                progress_callback(90, "正在保存结果...")
            
            # 更新录音信息
            self.db.update_recording_analysis(
                recording_id,
                analysis["keywords"],
                analysis["summary"],
                analysis["todos"],
                analysis["sentiment"]
            )
            
            # 添加转写内容
            self.db.add_transcript(recording_id, segments)
            
            # 添加说话人
            speakers = [
                {"id": spk_id, "name": f"说话人{i+1}"}
                for i, spk_id in enumerate(speaker_stats.keys())
            ]
            self.db.add_speakers(recording_id, speakers)
            
            # 更新状态为完成
            self.db.update_recording_status(recording_id, "completed")
            
            if progress_callback:
                progress_callback(100, "处理完成！")
            
            print(f"\n{'='*50}")
            print(f"处理完成！ID: {recording_id}")
            print(f"{'='*50}\n")
            
            return recording_id
            
        except Exception as e:
            print(f"处理失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 更新状态为错误
            self.db.update_recording_status(recording_id, "error")
            
            raise
    
    def close(self):
        """关闭资源"""
        self.db.close()
