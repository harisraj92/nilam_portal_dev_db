import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        user='nilam_insights_admin',
        password='Terra_Insights_2025',
        database='nilam_insights_dev',
        host='nilam-insights.postgres.database.azure.com',
        port=5432,
        ssl='require'
    )
    print("✅ Connected successfully!")
    await conn.close()

asyncio.run(test())
