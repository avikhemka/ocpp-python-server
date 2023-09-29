import asyncio
import logging
from ocpp.v201 import ChargePoint as cp
import websockets
import ocpp.v201.call as call

print(help(call.AuthorizePayload))
logging.basicConfig(level=logging.INFO)

class Charger(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={
                "model": "Wallbox XYZ",
                "vendor_name": "anewone",
            },
            reason="PowerUp",
        )
        response = await self.call(request)

        if response.status == "Accepted":
            print("Connected to central system.")

    async def send_authorize(self, id_tag):
        token = {"id_token_type": "ISO14443", "id_token": id_tag}
        request = call.AuthorizePayload(id_token=token)
        response = await self.call(request)

        if response.status == "Accepted":
            print(f"Authorization accepted for tag: {id_tag}")
        else:
            print(f"Authorization denied for tag: {id_tag}")

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()
        response = await self.call(request)

        print(f"Received heartbeat response with current time: {response.current_time}")

async def main():
    async with websockets.connect(
        'ws://175.41.149.142:9000/CP_1',  # Changed to AWS IP
        subprotocols=['ocpp2.0.1']
    ) as ws:
        charger = Charger('CP_1', ws)

        await asyncio.gather(
            charger.start(),
            charger.send_boot_notification(),
            charger.send_authorize("123456"),
            charger.send_heartbeat(),
        )

if __name__ == '__main__':
    asyncio.run(main())