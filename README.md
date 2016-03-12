java-rpms
===========

Script and rpm spec file to build smart "custom" rpms, to allow automatic upgrades across environment.

Legality
-------------
According to [Oracle's License](http://www.oracle.com/technetwork/java/javase/terms/license/index.html) it is illegal to redistribute RPMs made from this.  Though you should be able to redistribute within your organization.

Instructions
-------------
1. Download necessary JDK and/or JRE tar.gz files from http://www.oracle.com/technetwork/java/javase/downloads/index.html
2. Place files in `./original`
3. Ensure `~/rpmbuild` is properly setup
4. run `./build.sh`
5. publish `~/rpmbuild/RPMS/*/*.rpm` in your yum repository
