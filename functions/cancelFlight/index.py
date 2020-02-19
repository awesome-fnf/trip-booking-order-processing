import json
import logging
import uuid

class CancelFlightError(Exception):
  pass

def handler(event, context):
  evt = json.loads(event)
  txn_id = evt['transaction_id']
  result = evt['result']
  logger = logging.getLogger()

  if result == "failed":
    logger.info("Cancel flight ticket failed, transaction_id %s", txn_id)
    raise CancelFlightError("Cancel flight ticket exception")
  logger.info("Cancel flight succeeded, transaction_id %s" % txn_id)
  return '{"cancel_flight_ticket":"success", "transaction_id": "%s"}' % txn_id