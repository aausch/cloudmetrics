from .. import MetricsAPI
from ..backends import MetricsBackend


class PrintMetricsBackend(MetricsBackend):

    def publish(self, items):
        for (name, value, unit) in items:
            if unit == 'None':
                print '{namespace}:{name} {value}'.format(
                    namespace=self.namespace,
                    name=name,
                    value=value,
                )
            else:
                print '{namespace}:{name} {unit}={value}'.format(
                    namespace=self.namespace,
                    name=name,
                    unit=unit,
                    value=value,
                )


# Create a metrics object with the custom backend.
metrics_api = MetricsAPI(PrintMetricsBackend)


# Now use it to print some junk.
with metrics_api('printmetrics') as metrics:
    metrics.push('debug', value='Hello from PrintMetricsBackend')
    metrics.push('speed', kilobytes_per_second=50)
