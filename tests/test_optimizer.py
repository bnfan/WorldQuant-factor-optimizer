"""
WorldQuant Factor Optimizer 测试文件
"""

import pytest
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gpt_optimizer import WorldQuantFactorOptimizer


class TestWorldQuantFactorOptimizer:
    """测试 WorldQuantFactorOptimizer 类"""
    
    def test_validate_factor_input(self):
        """测试因子输入验证"""
        optimizer = WorldQuantFactorOptimizer.__new__(WorldQuantFactorOptimizer)
        
        # 测试有效因子
        valid_factors = [
            "ts_corr(rank(open), rank(volume), 10)",
            "rank(close - open)",
            "ts_mean(close, 20)",
            "zscore(volume)"
        ]
        
        for factor in valid_factors:
            assert optimizer.validate_factor_input(factor) == True
        
        # 测试无效因子
        invalid_factors = [
            "",  # 空字符串
            "invalid_function()",  # 无效函数
            "ts_corr(rank(open), rank(volume), 10",  # 括号不匹配
            "a" * 200  # 过长表达式
        ]
        
        for factor in invalid_factors:
            assert optimizer.validate_factor_input(factor) == False
    
    def test_load_operators(self):
        """测试操作符加载"""
        optimizer = WorldQuantFactorOptimizer.__new__(WorldQuantFactorOptimizer)
        
        # 测试文件存在的情况
        operators = optimizer.load_operators()
        assert isinstance(operators, str)
        assert len(operators) > 0
        assert "ts_corr" in operators
        assert "rank" in operators
    
    def test_get_default_suggestions(self):
        """测试默认建议生成"""
        optimizer = WorldQuantFactorOptimizer.__new__(WorldQuantFactorOptimizer)
        optimizer.original_factor = "ts_corr(rank(open), rank(volume), 10)"
        
        suggestions = optimizer.get_default_suggestions()
        
        assert isinstance(suggestions, list)
        assert len(suggestions) == 5
        
        for suggestion in suggestions:
            assert 'description' in suggestion
            assert 'expression' in suggestion
            assert isinstance(suggestion['description'], str)
            assert isinstance(suggestion['expression'], str)
            assert len(suggestion['description']) > 0
            assert len(suggestion['expression']) > 0


if __name__ == "__main__":
    pytest.main([__file__])
