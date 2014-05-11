#!/bin/bash

EXT_RELEASE=${BUILDNUMBER-$(date +%s)}
umask 022
echo "Release: ${EXT_RELEASE}"

for GZ in $(find original -type f -exec basename {} \;); do
  EXT_TAG=$(echo $GZ | cut -f 1 -d-)
  ARCH=$(echo $GZ | grep -oE "(i586|x64)")
  VER=$(echo $GZ | grep -oE "8u[0-9][0-9]*"|cut -f 2 -du)
  DIR="1.8.0_$(printf "%02d" $VER)"

  EXT_PRIORITY=1801
  if [ "${EXT_TAG}" == "jdk" ]; then
    PROVIDES="java-devel"
    EXT_PRIORITY=1800
  fi

  case $ARCH in
  i586)
	export EXT_ARCH=i686
	;;
  x64)
        export EXT_ARCH=x86_64
	;;
  esac

  export EXT_SOURCE=$GZ
  export EXT_VERSION="1.8.0.${VER}"
  echo "$GZ -> $EXT_ARCH,$EXT_VERSION"
  cp -v deployment.properties ~/rpmbuild/SOURCES
  cp -v original/$GZ ~/rpmbuild/SOURCES

  rpmbuild -ba -v --target $EXT_ARCH -D "oraver ${DIR}" -D "priority ${EXT_PRIORITY}" -D "ext_provides ${PROVIDES}" -D "ext_tag ${EXT_TAG}" -D "ext_arch ${EXT_ARCH}" -D "ext_version ${EXT_VERSION}" -D "ext_source ${GZ}" -D "ext_release ${EXT_RELEASE}" --define '__os_install_post \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:/usr/lib/rpm/redhat/brp-strip %{__strip}} \
    /usr/lib/rpm/redhat/brp-strip-shared %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}' java.spec &
done | cat
if [ "$PROMOTE" == "y" ]; then
find ~/rpmbuild/RPMS -type f -exec sudo mv -v {} /opt/rpm \;
cd /opt/rpm
sudo createrepo .
sudo yum clean all
fi
