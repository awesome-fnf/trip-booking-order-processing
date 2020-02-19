import json
import logging
import uuid

class BookFlightError(Exception):
  pass

def handler(event, context):
  evt = json.loads(event)
  txn_id = uuid.uuid4()
  result = evt['result']
  logger = logging.getLogger()

  if result == "failed":
    logger.info("Book flight failed, transaction_id %s", txn_id)
    raise BookFlightError("Book flight exception")
  logger.info("Book flight succeeded, transaction_id %s" % txn_id)
  return '{"book_flight":"success", "transaction_id": "%s"}' % txn_id