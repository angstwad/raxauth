## RaxAuth

A simple module to authenticate against the Rackspace Cloud Identity (Keystone).

Implementation is simple but still leaves a bit to be desired at the moment:

    a = raxauth.auth('username', 'apikey')
    print a.getToken()
    print a.getOSServerEndpoint()
    print a.getServerEndpoint()
    print a.getFilesEndpoint()
    print a.getLoadBalEndpoint()
    print a.getFilesCDNEndpoint()
    print a.getDBEndpoint()
    print a.getCloudDNS()
    print a.getCloudMonitoring()

Returns:
	
    https://dfw.servers.api.rackspacecloud.com/v2/5555555
    https://servers.api.rackspacecloud.com/v1.0/5555555
    https://storage101.dfw1.clouddrive.com/v1/MossoCloudFS_some-long-UUID
    https://dfw.loadbalancers.api.rackspacecloud.com/v1.0/5555555
    https://cdn1.clouddrive.com/v1/MossoCloudFS_some-long-UUID
    https://dfw.databases.api.rackspacecloud.com/v1.0/5555555
    https://dns.api.rackspacecloud.com/v1.0/5555555
    https://monitoring.api.rackspacecloud.com/v1.0/555555

The methods return data as strings depending on what you're looking for.  The default will return the proper endpoint URL from your default datacenter, but you can get *everything*, *or* you can get just an endpoint.  It'll also return exacltly the key you're looking for from the appropriate service!

    print a.getOSServerEndpoint(region='ORD')
    print a.getOSServerEndpoint(region='ORD', key='versionInfo')

Returns:

	https://ord.servers.api.rackspacecloud.com/v2/555555
	https://ord.servers.api.rackspacecloud.com/v2

**Works like a champ.**  Or so I think.  

Its supposed to just be useful, so if it sucks… It'll break my heart, but it's time to fix it.  Shoot me an email, and please give it some love and use it.  

*I am not a Python programmer.*  I am just a dude that loves code, the cloud, and APIs.  Pull requests welcome or I'd put the code elsewhere.

Emails welcome to **pauldurivage at gmail dot com**
