
from gpt_optimizer import WorldQuantFactorOptimizer

express = '-ts_mean((close/open - 1), 20))'

# 创建优化器实例
optimizer = WorldQuantFactorOptimizer(express)

# 运行优化流程
optimizer.run_optimization()