from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

def push_metrics_pushgateway(metric_name,
metric_desc,
pushgateway_url,
value,
labels,
job="google-cloud-functions"):
  """
  Pushes a metric to a Prometheus PushGateway instance.
  :param string metric_name: Metric name to use
  :param string metric_desc: Metric description
  :param string pushgateway_url: A PushGateway URL in the form of http://pushgateway:9091
  :param float64 value: Metric value
  :param dict labels:
  :param string job:
  """
  registry = CollectorRegistry()

  _label_keys = []
  _label_values = []
  for key,val in labels.items():
      _label_keys.append(key)
      _label_values.append(val)

  g = Gauge(metric_name, metric_desc, _label_keys, registry=registry)
  g.labels(tuple(_label_values)).set(value)

  try:
      push_to_gateway(pushgateway_url, job=job, registry=registry)
  except Exception as e:
      print(f"Error: {e}")
      return e
