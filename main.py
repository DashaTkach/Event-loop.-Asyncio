import asyncio
import aiohttp
from more_itertools import chunked

from models import init_db, Session, SwapiPeople

MAX_CHUNK = 10


async def get_person(person_id, session):
    http_response = await session.get(f"https://swapi.dev/api/people/{person_id}/")
    json_data = await http_response.json()
    return json_data


async def insert_records(records):
    for record in records:
        for position in record:
            element = SwapiPeople(birth_year=position['birth_year'], eye_color=position['eye_color'],
                                  films=position['films'], gender=position['gender'], hair_color=position['hair_color'],
                                  height=position['height'], homeworld=position['homeworld'], mass=position['mass'],
                                  name=position['name'], skin_color=position['skin_color'], species=position['species'],
                                  starships=position['starships'], vehicles=position['vehicles']
                                  )
            async with Session() as session:
                session.add_all(element)
                await session.commit()

async def main():
    await init_db()
    session = aiohttp.ClientSession()
    for people_id_chunk in chunked(range(1, 100), MAX_CHUNK):
        coros = [get_person(person_id, session) for person_id in people_id_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_records(result))

    await session.close()
    all_tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*all_tasks_set)


asyncio.run(main())
