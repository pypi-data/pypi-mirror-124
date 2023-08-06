from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

def push_metrics_pushgateway(metric_name,
metric_desc,
pushgateway_url,
value,
labels,
job="google-cloud-functions"):
  registry = CollectorRegistry()

  _label_keys = []
  _label_values = []
  for key,val in labels.items():
      _label_keys.append(key)
      _label_values.append(val)

  g = Gauge(metric_name, metric_desc, _label_keys, registry=registry)
  g.labels(f"{','.join(val for val in _label_values)}").set(value)

  try:
      push_to_gateway(pushgateway_url, job=job, registry=registry)
  except Exception as e:
      print(f"Error: {e}")
      return e
