
import aio_pika
from aio_pika.abc import AbstractRobustConnection
from db.models.user import User
from db.session import async_session_maker
from sqlalchemy import insert

async def consume_user_created_events(rabbitmq_url: str):
    
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()
    
    
    exchange = await channel.declare_exchange(
        "user_events", 
        type="direct",
        durable=True  
    )
    
    
    queue = await channel.declare_queue(
        "user_profile_queue",
        durable=True
    )
    
    
    await queue.bind(exchange, routing_key="user.created")
    
    print("🚀 Profile service consumer started. Waiting for messages...")
    
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                user_id = int(message.body.decode())
                print(f"📩 Received user_created event for user_id: {user_id}")
                
                async with async_session_maker() as session:
                    try:
                        
                        stmt = insert(User).values(id=user_id)
                        await session.execute(stmt)
                        await session.commit()
                        print(f"✅ Created profile for user {user_id}")
                    except Exception as e:
                        print(f"❌ Failed to create profile: {e}")
                        await session.rollback()