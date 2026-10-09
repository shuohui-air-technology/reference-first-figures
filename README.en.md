# Reference-first Figures — User Guide

[中文](README.md)

Extract actionable design relationships from paper figures that have actually been looked at, draw with reference to real scientific figures, and then revise against the exported result. This prevents an AI from drawing speculatively without understanding how the corresponding figures are actually used.

Applies to new or substantially redesigned scientific figures, including statistical plots, maps, method flows, model schematics, and composite figures.

## Invocation examples

```text
使用 reference-first-figures 为这张方法图寻找并实际查看可比参考，
根据我的模型结构提出可执行的设计，再基于真实材料绘制与对照修订。
```

```text
Use reference-first-figures to find and inspect comparable method diagrams,
derive an actionable design from my model, then draw from my materials and
compare the exported result with the references.
```

Using it requires the model structure, source data or existing figure, plus the design, tools, and delivery format to preserve. When only a design is needed, ask for planning first; small fixes such as labels or spacing automatically continue with the current tool. The full workflow is in [SKILL.md](SKILL.md).
