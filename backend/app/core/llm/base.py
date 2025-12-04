from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    async def generate_rfp_structure(self, text: str):
        pass

    @abstractmethod
    async def extract_vendor_proposal(self, raw_text: str):
        pass
