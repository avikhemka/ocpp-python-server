import asyncio
import logging
from datetime import datetime

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from ocpp.v201.enums import RegistrationStatusType
from ocpp.v201 import call

import websockets

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    async def send_boot_notification(self, conf):
        await self.send_call_result('BootNotification', conf)

    @on('BootNotification')
    def on_boot_notification(self, charging_station, reason, **kwargs):
        print(f"Received boot notification from {charging_station.vendor_name}, model {charging_station.model}")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatusType.accepted,
        )

    @on(call.AuthorizePayload)
    def on_authorize(self, id_tag, **kwargs):
        print(f"Received authorize request for tag: {id_tag}")

        # Implement your authorization logic here

        return call_result.AuthorizePayload(
            status="Accepted"  # Or "Rejected" based on your authorization logic
        )

    @on(call.HeartbeatPayload)
    def on_heartbeat(self, **kwargs):
        print("Received heartbeat request")

        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

async def on_connect(websocket, path):
    logging.info('WebSocket Server Started')
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


server = websockets.serve(on_connect, '0.0.0.0', 9000, subprotocols=['ocpp2.0.1'])

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()