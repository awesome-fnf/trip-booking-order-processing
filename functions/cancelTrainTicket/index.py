import json
import logging
import uuid

class CancelTrainTicketError(Exception):
  pass

def handler(event, context):
  evt = json.loads(event)
  txn_id = evt['transaction_id']
  result = evt['result']
  logger = logging.getLogger()

  if result == "failed":
    logger.info("Cancel train ticket failed, transaction_id %s", txn_id)
    raise CancelTrainTicketError("Cancel train ticket exception")
  logger.info("Cancel train ticket succeeded, transaction_id %s" % txn_id)
  return '{"cancel_train_ticket":"success", "transaction_id": "%s"}' % txn_id