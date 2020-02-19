import json
import logging

def handler(event, context):
  evt = json.loads(event)
  order_id = evt['trip_order_id']
  email_addr = evt['alert_email_address']
  logger = logging.getLogger()

  logger.info('Notified %s for failed order %s' % (email_addr, order_id))
  return '{"result":"success"}'