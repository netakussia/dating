class NSFWService:
    """Safety extension point. Override `score` with an ONNX/service-backed classifier."""
    def __init__(self, threshold: float = 0.85) -> None: self.threshold = threshold
    async def score(self, photo_file_id: str) -> float: return 0.0
    async def is_allowed(self, photo_file_id: str) -> bool: return await self.score(photo_file_id) < self.threshold
