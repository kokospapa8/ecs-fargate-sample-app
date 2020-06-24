# -*- coding: utf-8 -*-
import asyncio, os
from django_rq import job

async def sleep():
    counter = 0
    while counter < 30:
        # suspend execution
        await asyncio.sleep(1000)
        print(counter)
        counter +=1
    return counter

@job("async")
def rq_test():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(sleep())
