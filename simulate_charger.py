import asyncio
import websockets
import json
from ocpp.v201 import call

async def simulate_charger():
    async with websockets.connect('ws://192.168.1.119:9000/', subprotocols=['ocpp2.0.1']) as websocket:
        try:
            request = call.BootNotificationPayload(
                charging_station={
                    'model': 'Wallbox XYZ',
                    'vendor_name': 'anewone'
                },
                reason="PowerUp"
            )
            request_dict = request.to_dict()
            await websocket.send(json.dumps(request_dict))
            response = await websocket.recv()
            print(f"Received response: {response}")

        except Exception as e:
            print(f"Error occurred: {e}")

asyncio.run(simulate_charger())