#!/bin/bash
# Tavily 搜索 + 使用计数追踪

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 调用原始脚本
python3 "$SCRIPT_DIR/tavily_search.py" "$@"
RESULT=$?

# 更新使用计数
if [ $RESULT -eq 0 ]; then
    python3 - << 'PYEOF'
import json
import pathlib
from datetime import datetime
import sys

state_path = pathlib.Path.home() / ".openclaw" / "workspace" / "memory" / "tavily-state.json"
state_path.parent.mkdir(parents=True, exist_ok=True)

now = datetime.now()
current_month = now.strftime("%Y-%m")

if state_path.exists():
    try:
        state = json.loads(state_path.read_text())
    except:
        state = {"monthly_limit": 1000, "used": 0, "month": current_month}
else:
    state = {"monthly_limit": 1000, "used": 0, "month": current_month}

if state.get("month") != current_month:
    state["used"] = 0
    state["month"] = current_month

state["used"] = state.get("used", 0) + 1
state["last_updated"] = now.isoformat()
state_path.write_text(json.dumps(state, indent=2))

if state["used"] % 20 == 0:
    remaining = state["monthly_limit"] - state["used"]
    print(f"\n📊 Tavily 已使用 {state['used']} 次，剩余 {remaining} 次", file=sys.stderr)
PYEOF
fi

exit $RESULT
