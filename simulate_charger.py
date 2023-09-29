import asyncio
import logging
from datetime import datetime

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys

    sys.exit(1)

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import AuthorizationStatus, ConnectorStatus, ErrorCode, RegistrationStatus

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    connector_status = ConnectorStatus.available
    transaction_id = None

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Charge", charge_point_vendor="GridFlow"
        )

        response = await self.call(request)

        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()
        response = await self.call(request)
        print('Heartbeat sent, central system responded with time: ', response.current_time)

    async def send_status_notification(self):
        request = call.StatusNotificationPayload(
            connector_id=1,
            error_code=ErrorCode.no_error,
            status=self.connector_status,
        )
        response = await self.call(request)
        print("Status Notification sent.")

    async def send_start_transaction(self):
        if self.connector_status == ConnectorStatus.available:
            self.connector_status = ConnectorStatus.occupied
            request = call.StartTransactionPayload(
                connector_id=1,
                id_tag="ABC123",
                meter_start=0,
                timestamp=datetime.utcnow().isoformat(),
            )
            response = await self.call(request)
            if response.id_tag_info.status == AuthorizationStatus.accepted:
                print("Start Transaction accepted.")
                self.transaction_id = response.transaction_id
            else:
                print("Start Transaction denied.")
        else:
            print("Connector not available.")

    async def send_stop_transaction(self):
        if self.connector_status == ConnectorStatus.occupied:
            self.connector_status = ConnectorStatus.available
            request = call.StopTransactionPayload(
                meter_stop=100,
                timestamp=datetime.utcnow().isoformat(),
                transaction_id=self.transaction_id,
            )
            response = await self.call(request)
            if response.id_tag_info:
                print("Stop Transaction accepted.")
            else:
                print("Stop Transaction denied.")
        else:
            print("No ongoing transaction.")


async def main():
    async with websockets.connect(
        "ws://175.41.149.142:9000/CP_1", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("CP_1", ws)

        await asyncio.gather(
            cp.start(),
            cp.send_boot_notification(),
            cp.send_heartbeat(),
            cp.send_status_notification(),
            cp.send_start_transaction(),
            asyncio.sleep(10),  # simulate a 10-second charging session
            cp.send_stop_transaction(),
        )


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())