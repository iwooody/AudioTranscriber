# -*- coding: utf-8 -*-
"""
语音识别模块 - 基于Whisper
"""

import whisper
import torch
import numpy as np
from pathlib import Path
import librosa
from typing import List, Dict
import warnings
warnings.filterwarnings("ignore")


class WhisperTranscriber:
    """Whisper语音识别器"""
    
    def __init__(self, model_name: str = "base", device: str = None):
        """
        初始化识别器
        
        Args:
            model_name: 模型名称 (tiny, base, small, medium, large)
            device: 计算设备 (cuda/cpu)，None则自动选择
        """
        self.model_name = model_name
        
        # 自动选择设备
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        print(f"正在加载Whisper模型: {model_name} (设备: {self.device})")
        
        try:
            self.model = whisper.load_model(model_name).to(self.device)
            print(f"模型加载完成")
        except Exception as e:
            print(f"模型加载失败: {e}")
            raise
    
    def transcribe(self, audio_path: str, language: str = "zh", 
                   progress_callback=None) -> Dict:
        """
        转录音频文件
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码 (zh, en, ja, ko等)
            progress_callback: 进度回调函数
            
        Returns:
            包含转写结果的字典
        """
        print(f"开始转写: {audio_path}")
        
        try:
            result = self.model.transcribe(
                audio_path,
                language=language if language != "auto" else None,
                verbose=False,
                word_timestamps=True
            )
            
            segments = []
            total_segments = len(result["segments"])
            
            for idx, seg in enumerate(result["segments"]):
                segments.append({
                    "id": idx,
                    "start": float(seg["start"]),
                    "end": float(seg["end"]),
                    "text": seg["text"].strip(),
                    "confidence": float(seg.get("avg_logprob", 0)),
                    "words": seg.get("words", [])
                })
                
                if progress_callback:
                    progress_callback(int((idx + 1) / total_segments * 100))
            
            return {
                "language": result.get("language", language),
                "full_text": result["text"],
                "segments": segments
            }
            
        except Exception as e:
            print(f"转写失败: {e}")
            raise
    
    def transcribe_long_audio(self, audio_path: str, language: str = "zh",
                              chunk_length: int = 30, 
                              progress_callback=None) -> Dict:
        """
        处理长音频（超过30分钟）
        分段处理避免内存溢出
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码
            chunk_length: 每段长度（秒）
            progress_callback: 进度回调函数
        """
        print(f"处理长音频: {audio_path}")
        
        # 获取音频时长
        try:
            duration = librosa.get_duration(path=audio_path)
            print(f"音频时长: {duration:.2f}秒")
        except Exception as e:
            print(f"无法获取音频时长: {e}")
            duration = 0
        
        if duration <= 0 or duration <= chunk_length * 60:
            # 如果音频不长，直接处理
            return self.transcribe(audio_path, language, progress_callback)
        
        # 长音频分段处理
        all_segments = []
        full_text_parts = []
        
        num_chunks = int(np.ceil(duration / (chunk_length * 60)))
        
        for i in range(num_chunks):
            start_time = i * chunk_length * 60
            end_time = min((i + 1) * chunk_length * 60, duration)
            
            print(f"处理段落 {i+1}/{num_chunks}: {start_time:.0f}s - {end_time:.0f}s")
            
            try:
                # 加载音频段落
                audio_chunk, sr = librosa.load(
                    audio_path,
                    offset=start_time,
                    duration=end_time - start_time,
                    sr=16000
                )
                
                # 转写
                result = self.model.transcribe(
                    audio_chunk,
                    language=language if language != "auto" else None
                )
                
                # 调整时间戳
                for seg in result["segments"]:
                    seg["start"] = float(seg["start"]) + start_time
                    seg["end"] = float(seg["end"]) + start_time
                    all_segments.append({
                        "id": len(all_segments),
                        "start": seg["start"],
                        "end": seg["end"],
                        "text": seg["text"].strip(),
                        "confidence": float(seg.get("avg_logprob", 0)),
                        "words": seg.get("words", [])
                    })
                
                full_text_parts.append(result["text"])
                
                if progress_callback:
                    progress_callback(int((i + 1) / num_chunks * 100))
                    
            except Exception as e:
                print(f"段落 {i+1} 处理失败: {e}")
                continue
        
        return {
            "language": language,
            "full_text": " ".join(full_text_parts),
            "segments": all_segments
        }
