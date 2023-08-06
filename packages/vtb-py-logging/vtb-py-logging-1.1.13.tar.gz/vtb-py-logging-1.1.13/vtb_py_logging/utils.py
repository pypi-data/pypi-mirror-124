import logging


def get_data_record(record: logging.LogRecord) -> tuple:
    order_action = getattr(record, 'order_action', {})
    order_id = order_action.get('order_id')
    action_id = order_action.get('action_id')
    graph_id = order_action.get('graph_id')
    node = getattr(record, 'node', None)
    action_type = getattr(record, 'action_type', None)
    orchestrator_id = getattr(record, 'orchestrator_id', None)
    return order_id, action_id, graph_id, node, action_type, orchestrator_id


def get_graph_logger(*, logger=None, logger_name=None, graph=None,
                     order_action=None, node=None, action_type=None, orchestrator_id=None):
    assert bool(logger) != bool(logger_name)  # please specify logger of logger_name
    if logger_name:
        logger = logging.getLogger(logger_name)

    if graph:
        extra = {
            "order_action": graph.order_action.__dict__,
            "node": graph.path,
            "orchestrator_id": graph.id
        }
    else:
        extra = {
            "order_action": order_action.__dict__,
            "node": node,
            "orchestrator_id": orchestrator_id
        }
    extra["action_type"] = action_type

    return logging.LoggerAdapter(logger, extra=extra)
