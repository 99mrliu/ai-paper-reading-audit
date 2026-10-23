# 原生JSONL导出的实际边界

14次原始events.jsonl均保留，未补写图片事件或工具调用。实际统计只纳入item.started中的command_execution、mcp_tool_call、web_search；这叫“可见调用”，不是完整内部执行事件或所有工具操作的保证。

检查新版本比较试验时发现：有实际页面渲染及报告视觉核查陈述，但CLI JSONL没有独立image-view条目。不能由条目缺失断言Agent未看到图，也不能把报告自述当完整独立接收日志。两者应分别保留；30次预算是给模型的任务约束，采集器并未在30次强制截断，且导出不足以独立审计所有内部调用。

核对了OpenAI公开原代码：codex-rs/exec/src/event_processor_with_jsonl_output.rs的map_item_with_id映射存在默认`_ => None`分支，在取得的代码中未找到ImageView映射。来源：https://github.com/openai/codex/blob/main/codex-rs/exec/src/event_processor_with_jsonl_output.rs ，取得的Git blob SHA：73e0c9d911c82aae67c44e6b1a4ce54c7092b6be。该公开main不是本机二进制的严格构建来源证明，因此这里以实际导出观察为准，不推断所有版本均如此。

本发现限制“完整调用审计”说法，不改变已经产生的原始报告、session耗时和原生usage，也不把缺失事件伪造成运行失败。后续若要严格证明视觉调用或强制调用预算，应使用能导出相应事件的采集方式，另开新版本；不能为旧记录补造细节。
