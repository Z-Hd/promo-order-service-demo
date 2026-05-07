# Promo Order Service Demo

一个适合 `WebServiceGuard-Agent` 演示的简单 Web 服务。

## 特点

- FastAPI 服务，接口少，易于展示
- 预埋了两个真实且稳定的后端 Bug
- 带测试，方便阶段二验证
- 日志默认写入 `logs/app.log`

## 接口

- `GET /health`
- `POST /orders/preview`

## 预埋 Bug

1. `ZeroDivisionError`
   当 `items=[]` 时，`app/services/pricing.py` 会执行除零。

2. `AttributeError`
   当 `coupon=null` 时，`app/services/pricing.py` 会访问 `payload.coupon.type`。

## 启动

```bash
cd /tmp/promo-order-service-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

如果你想把 traceback 直接写进日志文件并便于阶段一抓取：

```bash
cd /tmp/promo-order-service-demo
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8001 >> logs/runtime.log 2>&1
```

## 触发 Bug

触发 `ZeroDivisionError`:

```bash
curl -X POST http://127.0.0.1:8001/orders/preview \
  -H "Content-Type: application/json" \
  -d '{"items":[],"coupon":{"type":"percent","value":10}}'
```

触发 `AttributeError`:

```bash
curl -X POST http://127.0.0.1:8001/orders/preview \
  -H "Content-Type: application/json" \
  -d '{"items":[{"sku":"A100","price":100,"quantity":1}],"coupon":null}'
```

## 测试

```bash
cd /tmp/promo-order-service-demo
source .venv/bin/activate
pytest -q
```

当前预期是：

- `test_health_ok` 和 `test_preview_order_with_valid_coupon` 通过
- 两个 “should_not_crash” 用例失败

## 适合你们当前系统的原因

- Traceback 清晰
- 修复点集中在单文件
- 很容易让 Agent 补边界处理
- 可以自然进入 “修复后测试转绿 -> PR -> 通知” 的完整展示
