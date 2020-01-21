# This is basicaly a commandline tool to get metric data
# from Jenkins Metric Plugin (https://wiki.jenkins-ci.org/display/JENKINS/Metrics+Plugin)
# Use it like example below:
#  python jenkins-metrics.py                             # To get all keys and values
# or
#  python jenkins-metrics.py timers.http.requests.p999   # To get only the value

import urllib, json, sys

metrics = {}
JENKINS_URL = "http://a59638eaefc8f11e99d8e0ac7f60df55-1872873982.eu-west-1.elb.amazonaws.com:8080/"
PLUGIN_KEY = "fTjFtcC0YFBe_jKT1UUoaTUImNRQP1AqNwrOzeJZBvYm7v5idzZzswWmh5BP4Bpq"

def denormalize(data, keyname):
    for d in data.keys():
        if isinstance(data[d], dict):
            denormalize(data[d], u"%s%s." % (keyname, d))
        else:
            metrics[u"%s%s" % (keyname, d)] = data[d]

if __name__ == "__main__":

    response = urllib.urlopen("%s/metrics/%s/metrics" % (JENKINS_URL, PLUGIN_KEY));
    data = json.loads(response.read())

    denormalize(data, u"")

    if len(sys.argv) > 1 :
        print metrics[str(sys.argv[1])]
    else:
        for m in metrics:
            print "%s=%s" % (m, metrics[m])
