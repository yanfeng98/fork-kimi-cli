import asyncio
import contextvars

user_context = contextvars.ContextVar("user_name", default="Guest")


def logic():
    current_user = user_context.get()
    print(f"当前用户: {current_user}")


logic()  # 输出: 当前用户: Guest

token = user_context.set("Alice")

logic()  # 输出: 当前用户: Alice

user_context.reset(token)

logic()  # 输出: 当前用户: Guest

request_id_var = contextvars.ContextVar("request_id")


async def process_request(req_id, delay):
    request_id_var.set(req_id)
    print(f"[开始] 处理请求 {req_id}, 上下文值已设为: {request_id_var.get()}")

    await asyncio.sleep(delay)

    current_val = request_id_var.get()
    print(f"[结束] 处理请求 {req_id}, 上下文值依然是: {current_val}")


async def main():
    await asyncio.gather(process_request(100, 0.1), process_request(200, 0.1))


if __name__ == "__main__":
    asyncio.run(main())
