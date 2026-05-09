import asyncio

class SwarmOrchestrator:
    def __init__(self):
        self.agents = []

    def register(self, agent):
        self.agents.append(agent)

    async def analyze(self, symbol):
        tasks = [agent.analyze(symbol) for agent in self.agents]
        results = await asyncio.gather(*tasks)
        return results
