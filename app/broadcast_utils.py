from broadcaster import Broadcast
from app.config import settings

broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)
