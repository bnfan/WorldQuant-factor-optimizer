
from gpt_optimizer import WorldQuantFactorOptimizer

express = '-ts_mean((close/open - 1), 20))'

#model = 'openai/gpt-5-chat'
model = 'anthropic/claude-sonnet-4'

# 创建优化器实例
optimizer = WorldQuantFactorOptimizer(model, express)

# 运行优化流程
optimizer.run_optimization()