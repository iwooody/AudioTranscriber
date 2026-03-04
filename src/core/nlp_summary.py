# -*- coding: utf-8 -*-
"""
NLP摘要模块
关键词提取、待办事项提取、情感分析
"""

import re
from typing import List, Dict
from collections import Counter
import jieba
import jieba.posseg as pseg


class NLPSummarizer:
    """NLP文本分析器"""
    
    def __init__(self):
        """初始化"""
        # 加载用户词典（如果有）
        pass
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        提取关键词
        
        Args:
            text: 输入文本
            top_n: 返回前N个关键词
            
        Returns:
            关键词列表
        """
        # 分词
        words = jieba.lcut(text)
        
        # 过滤停用词和单字
        stop_words = set([
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", 
            "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
            "你", "会", "着", "没有", "看", "好", "自己", "这", "那"
        ])
        
        filtered_words = [
            w for w in words 
            if len(w) > 1 and w not in stop_words
        ]
        
        # 统计词频
        word_counts = Counter(filtered_words)
        
        # 返回前N个
        return [word for word, _ in word_counts.most_common(top_n)]
    
    def extract_todos(self, segments: List[Dict]) -> List[Dict]:
        """
        提取待办事项
        
        Args:
            segments: 转写段落列表
            
        Returns:
            待办事项列表
        """
        # 待办关键词
        todo_keywords = [
            "需要", "必须", "应该", "安排", "准备", "完成", "落实",
            "负责", "跟进", "处理", "解决", "确认", "提交", "汇报",
            "记得", "别忘了", "一定", "务必", "赶紧", "尽快"
        ]
        
        todos = []
        
        for seg in segments:
            text = seg["text"]
            
            # 检查是否包含待办关键词
            if any(kw in text for kw in todo_keywords):
                # 提取包含关键词的句子
                sentences = re.split(r'[。！？；\n]', text)
                
                for sent in sentences:
                    sent = sent.strip()
                    if len(sent) < 5:
                        continue
                    
                    if any(kw in sent for kw in todo_keywords):
                        todos.append({
                            "text": sent,
                            "time": seg.get("start", 0),
                            "speaker": seg.get("speaker", "未知"),
                            "segment_id": seg.get("id", 0)
                        })
        
        # 去重
        seen = set()
        unique_todos = []
        for todo in todos:
            if todo["text"] not in seen:
                seen.add(todo["text"])
                unique_todos.append(todo)
        
        return unique_todos[:20]  # 最多返回20条
    
    def analyze_sentiment(self, segments: List[Dict]) -> Dict[str, Dict]:
        """
        简单的情感分析
        
        Returns:
            每个说话人的情感统计
        """
        # 情感词典
        positive_words = [
            "好", "棒", "优秀", "成功", "满意", "开心", "高兴", "不错",
            "赞成", "同意", "支持", "完美", "顺利", "轻松", "愉快"
        ]
        
        negative_words = [
            "差", "糟糕", "失败", "问题", "困难", "麻烦", "担心", "不好",
            "反对", "拒绝", "错误", "严重", "紧急", "焦虑", "生气"
        ]
        
        speaker_sentiments = {}
        
        for seg in segments:
            speaker = seg.get("speaker", "未知")
            text = seg["text"]
            
            if speaker not in speaker_sentiments:
                speaker_sentiments[speaker] = {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            
            # 统计情感词
            pos_count = sum(1 for w in positive_words if w in text)
            neg_count = sum(1 for w in negative_words if w in text)
            
            if pos_count > neg_count:
                speaker_sentiments[speaker]["positive"] += 1
            elif neg_count > pos_count:
                speaker_sentiments[speaker]["negative"] += 1
            else:
                speaker_sentiments[speaker]["neutral"] += 1
        
        # 计算占比
        for speaker in speaker_sentiments:
            total = sum(speaker_sentiments[speaker].values())
            if total > 0:
                for key in speaker_sentiments[speaker]:
                    speaker_sentiments[speaker][key] = round(
                        speaker_sentiments[speaker][key] / total * 100, 1
                    )
        
        return speaker_sentiments
    
    def generate_summary(self, full_text: str, max_sentences: int = 3) -> str:
        """
        生成文本摘要（抽取式）
        
        Args:
            full_text: 完整文本
            max_sentences: 摘要句子数
            
        Returns:
            摘要文本
        """
        # 分句
        sentences = re.split(r'[。！？\n]', full_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) <= max_sentences:
            return "。".join(sentences) + "。"
        
        # 计算句子权重（基于词频）
        # 统计全局词频
        word_freq = Counter(jieba.lcut(full_text))
        
        sentence_scores = []
        for sent in sentences:
            words = jieba.lcut(sent)
            score = sum(word_freq[w] for w in words if len(w) > 1)
            score = score / len(words) if words else 0
            sentence_scores.append((sent, score))
        
        # 按权重排序，取前N句
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:max_sentences]]
        
        # 按原文顺序排列
        top_sentences.sort(key=lambda s: full_text.index(s))
        
        return "。".join(top_sentences) + "。"
    
    def analyze_all(self, segments: List[Dict], full_text: str) -> Dict:
        """
        执行所有NLP分析
        
        Returns:
            包含所有分析结果的字典
        """
        print("正在进行NLP分析...")
        
        return {
            "keywords": self.extract_keywords(full_text, top_n=10),
            "todos": self.extract_todos(segments),
            "sentiment": self.analyze_sentiment(segments),
            "summary": self.generate_summary(full_text, max_sentences=3)
        }
