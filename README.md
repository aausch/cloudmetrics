cloudmetrics 0.0.1
==================

A Python library for sending metrics to CloudWatch.

Currently, this library only includes support for CloudWatch, but custom
backends can be easily created and used.


Installation
------------

    pip install cloudmetrics

Usage
-----

    # Create a metrics object once to use in your project.
    from cloudmetrics import MetricsAPI
    from cloudmetrics.backends.cloudwatch_backend import CloudWatchMetricsBackend
    metrics_api = MetricsAPI(CloudWatchMetricsBackend)

    # Use your metrics object to send metrics.
    with metrics_api(metric_namespace) as metrics:
        metrics.push(metric_name, **{unit: value})


Namespaces and Names
--------------------

All metrics must use a namespace and name, which must both be strings.


Units
-----

The push method requires a single unit/value pair.

Allowed unit types:

    seconds, microseconds, milliseconds,

    percent,

    count, count_per_second

    bytes, bytes_per_second
    kilobytes, kilobytes_per_second
    megabytes, megabytes_per_second
    gigabytes, gigabytes_per_second
    terabytes, terabytes_per_second

    bits, bits_per_second
    kilobits, kilobits_per_second
    megabits, megabits_per_second
    gigabits, gigabits_per_second
    terabits,terabits_per_second

    value (unspecified unit type)

Example usage:

    with metrics_api(metric_namespace) as metrics:
        metrics.push(metric_name, count=50)
        metrics.push(metric_name2, megabytes=3)
        metrics.push(metric_name3, value='hello')


Hostnames
---------

Metrics can be dimensioned using the current hostname if the backend supports
it. The CloudWatch backend supports hostnames.

Example usage:

    with metrics_api(metric_namespace, use_hostname=True) as metrics:
        metrics.push(metric_name, **{unit: value})

    or

    with metrics_api(metric_namespace) as metrics:
        metrics.use_hostname()
        metrics.push(metric_name, **{unit: value})

    or

    with metrics_api(metric_namespace, use_hostname='dogs.info') as metrics:
        metrics.push(metric_name, **{unit: value})

    or

    with metrics_api(metric_namespace) as metrics:
        metrics.use_hostname('buffalo.info')
        metrics.push(metric_name, **{unit: value})


Buffering
---------

Metrics backends can support buffering/batch requests, to publish multiple
metric data points with a single operation. This works automatically.

Amazon's CloudWatch API supports up to 10 metric data points per call, so the
CloudWatch backend buffers data accordingly. For example, making 15 calls to
**push()** within a context will result in one API call with the first 10 items,
and another with the remaining 5 items. API calls are made when the buffer
is full, and when the metrics context exits with a non-empty buffer.


Custom Backends
---------------

It is easy to create custom metrics backends. This example will print metrics
to standard output:

    from cloudmetrics import MetricsAPI
    from cloudmetrics.backends import MetricsBackend

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

Which looks like:

    $ python -m cloudmetrics.examples.printmetrics
    printmetrics:debug Hello from PrintMetricsBackend
    printmetrics:speed Kilobytes/Second=50


Fallback Backends
-----------------

If CloudWatch cannot be accessed for whatever reason, it might be a good idea
to write the metrics to an alternate location as a fallback. It would be easy
to write a custom backend that writes to a log file, similar to the
PrintMetricsBackend example.

Example usage:

    metrics_api = MetricsAPI(
        backend_class=CloudWatchMetricsBackend,
        fallback_backend_class=LogFileMetricsBackend,
    )


Running unit tests
------------------

    python -m cloudmetrics.tests
