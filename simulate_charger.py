import asyncio
import json
import websockets

async def simulate_charger():
    async with websockets.connect('ws://192.168.1.119:9000/') as websocket:
        # Send a BootNotification message
        boot_notification_request = {
            "messageTypeId": 2,
            "uniqueId": "1234",
            "payload": {
                "chargePointModel": "TestCharger",
                "chargePointVendor": "ACME",
                "chargePointSerialNumber": "123456789",
                "chargeBoxSerialNumber": "123456789",
                "firmwareVersion": "1.0",
            }
        }

        await websocket.send(json.dumps(boot_notification_request))
        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.run(simulate_charger())
