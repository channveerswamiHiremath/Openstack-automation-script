# Openstack-automation-script
Automated background file synchronization to OpenStack Swift using Python

It is a Python-based automation script that continuously monitors a local folder and automatically uploads newly added files to openstack swift object storage. It uses keystone v3 authentication and securely retrieves credentials through environment variables instead of hardcoding them. The script runs in the background (.pyw format) and checks for new files every 4 minutes, ensuring periodic and reliable synchronization with the cloud.

After successfully uploading files to the configured swift container, the script automatically moves them to a “Sent” directory to prevent duplicate uploads. This implementation demonstrates practical OpenStack integration, scheduled background automation, and a real-world cloud storage workflow similar to enterprise backup and object storage synchronization systems.
