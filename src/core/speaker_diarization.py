# -*- coding: utf-8 -*-
"""
说话人分离模块
简化版实现（不依赖pyannote，使用聚类算法）
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.cluster import AgglomerativeClustering
import librosa
from pathlib import Path


class SimpleSpeakerDiarizer:
    """
    简化版说话人分离器
    基于音频特征的聚类算法
    """
    
    def __init__(self, num_speakers: int = None):
        """
        初始化
        
        Args:
            num_speakers: 说话人数量，None则自动检测
        """
        self.num_speakers = num_speakers
    
    def extract_features(self, audio_path: str, segments: List[Dict]) -> np.ndarray:
        """
        从音频段提取特征
        
        Returns:
            特征矩阵 (n_segments, n_features)
        """
        features = []
        
        try:
            # 加载音频
            audio, sr = librosa.load(audio_path, sr=16000)
            
            for seg in segments:
                start_sample = int(seg["start"] * sr)
                end_sample = int(seg["end"] * sr)
                
                # 确保索引有效
                start_sample = max(0, start_sample)
                end_sample = min(len(audio), end_sample)
                
                if end_sample <= start_sample:
                    features.append(np.zeros(20))  # 静音段
                    continue
                
                # 提取音频段
                segment_audio = audio[start_sample:end_sample]
                
                if len(segment_audio) < sr * 0.5:  # 少于0.5秒
                    features.append(np.zeros(20))
                    continue
                
                # 提取MFCC特征
                mfcc = librosa.feature.mfcc(
                    y=segment_audio,
                    sr=sr,
                    n_mfcc=20
                )
                
                # 计算统计特征
                mfcc_mean = np.mean(mfcc, axis=1)
                mfcc_std = np.std(mfcc, axis=1)
                
                # 组合特征
                seg_features = np.concatenate([mfcc_mean, mfcc_std])
                features.append(seg_features)
                
        except Exception as e:
            print(f"特征提取失败: {e}")
            # 返回零特征
            features = [np.zeros(40) for _ in segments]
        
        return np.array(features)
    
    def diarize(self, audio_path: str, segments: List[Dict]) -> List[Dict]:
        """
        执行说话人分离
        
        Args:
            audio_path: 音频文件路径
            segments: 转写段落列表
            
        Returns:
            添加了speaker_id的段落列表
        """
        print("开始说话人分离...")
        
        if len(segments) < 2:
            # 段落太少，无法分离
            for seg in segments:
                seg["speaker"] = "SPEAKER_00"
            return segments
        
        try:
            # 提取特征
            features = self.extract_features(audio_path, segments)
            
            # 确定聚类数量
            if self.num_speakers is None:
                # 自动检测：根据段落数量估计
                # 假设每人至少说5句话
                estimated_speakers = max(2, min(len(segments) // 5, 5))
                n_clusters = estimated_speakers
            else:
                n_clusters = self.num_speakers
            
            n_clusters = min(n_clusters, len(segments))
            
            print(f"检测到 {n_clusters} 个说话人")
            
            # 聚类
            clustering = AgglomerativeClustering(
                n_clusters=n_clusters,
                metric='euclidean',
                linkage='ward'
            )
            
            labels = clustering.fit_predict(features)
            
            # 分配说话人ID
            for i, seg in enumerate(segments):
                seg["speaker"] = f"SPEAKER_{labels[i]:02d}"
            
            return segments
            
        except Exception as e:
            print(f"说话人分离失败: {e}")
            # 失败时全部标记为同一人
            for seg in segments:
                seg["speaker"] = "SPEAKER_00"
            return segments
    
    def get_speaker_stats(self, segments: List[Dict]) -> Dict[str, float]:
        """
        获取说话人统计信息
        
        Returns:
            每个说话人的发言时长占比
        """
        speaker_times = {}
        total_time = 0
        
        for seg in segments:
            speaker = seg.get("speaker", "UNKNOWN")
            duration = seg["end"] - seg["start"]
            
            if speaker not in speaker_times:
                speaker_times[speaker] = 0
            speaker_times[speaker] += duration
            total_time += duration
        
        # 计算占比
        if total_time > 0:
            for speaker in speaker_times:
                speaker_times[speaker] = speaker_times[speaker] / total_time * 100
        
        return speaker_times
