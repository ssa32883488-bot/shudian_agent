# -*- coding: utf-8 -*-
from app.tools.draw_workflow.logic_fallback import fallback_logic_dag_script


def test_logic_fallback_and_nor_example():
    brief = "逻辑符号图示例：A、B经与门得Y1，Y1与C经或非门输出Y"
    script = fallback_logic_dag_script(brief=brief, slots={})
    assert script, "should parse Chinese AND+NOR steps"
    import json

    ir = json.loads(script)
    assert ir["schema_version"] == "logic_ir_v1"
    assert "A" in ir["inputs"] and "B" in ir["inputs"] and "C" in ir["inputs"]
    assert ir["gates"]
    types = {g["type"] for g in ir["gates"].values()}
    assert "AND" in types and "NOR" in types
