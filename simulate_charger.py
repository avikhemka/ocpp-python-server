import asyncio
import websockets
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
            await websocket.send(request.to_json())
            response = await websocket.recv()
            print(f"Received response: {response}")

        except Exception as e:
            print(f"Error occurred: {e}")

asyncio.run(simulate_charger())