import json
import logging
import uuid

class BookTrainTicketError(Exception):
  pass

def handler(event, context):
  evt = json.loads(event)
  txn_id = uuid.uuid4()
  result = evt['result']
  logger = logging.getLogger()

  if result == "failed":
    logger.info("Booke train failed, transaction_id %s", txn_id)
    raise BookTrainTicketError("Book train ticket exception")
  logger.info("Book train succeeded, transaction_id %s" % txn_id)
  return '{"book_train_ticket":"success", "transaction_id": "%s"}' % txn_id