import asyncio
from datetime import datetime
from ocpp.routing import on
from ocpp.v20 import ChargePoint as cp
from ocpp.v20 import call_result, call
from websockets import serve
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ocpp_server")

class ChargePoint(cp):
    @on(call.BootNotification)
    def on_boot_notification(self, charging_station, reason, **kwargs):
        print(f"Received BootNotification from charging station: {charging_station}")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            interval=10,
            status="Accepted"
        )

async def on_connect(websocket, path):
    try:
        charge_point = ChargePoint("my_charge_point", websocket)
        await charge_point.start()
    except Exception as e:
        logger.exception(f"Error occurred: {e}")

server = serve(on_connect, "0.0.0.0", 9000)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
