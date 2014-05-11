Name:		%{ext_tag}-1.8.0-oracle
Version:	%{ext_version}
Release:	%{ext_release}
Summary:	Java
Prefix:         /usr/java

License:	Oracle Binary Code License
Group:		Development/Tools
Source0:	%{ext_source}
Provides:       jre java %{ext_provides}
AutoReqProv:    no

%define javahome %{prefix}/8/%{ext_arch}/%{ext_tag}
%define javabin %{javahome}/bin
%define javaman %{javahome}/man/man1
%define rpmjhome $RPM_BUILD_ROOT%{javahome} 
%define filesspec %{ext_tag}-files.%{ext_arch}.spec
%define postsh %{ext_tag}.%{ext_arch}.sh

%description


%install
mkdir -p $RPM_BUILD_ROOT/usr/java/8/%{ext_arch}
tar -zxf $RPM_SOURCE_DIR/%{ext_source} -C $RPM_BUILD_ROOT/usr/java/8/%{ext_arch}
mv $RPM_BUILD_ROOT/usr/java/8/%{ext_arch}/%{ext_tag}%{oraver} $RPM_BUILD_ROOT/usr/java/8/%{ext_arch}/%{ext_tag}
cat $RPM_SOURCE_DIR/deployment.properties > $RPM_BUILD_ROOT%{javahome}/lib/deployment.properties
echo "deployment.system.config.mandatory=false
deployment.system.config=file:%{javahome}/lib/deployment.properties" > $RPM_BUILD_ROOT%{javahome}/lib/deployment.config
# Remove non-platform specific files
find %{rpmjhome} -name \*.bat -delete

#STRIP Binaries
strip -s $(find $RPM_BUILD_ROOT%{javahome} -type f -exec file {} \; |grep "not stripped$" |cut -f 1 -d:)

#COMPRESS man pages
find $RPM_BUILD_ROOT%{javahome} -type f -name \*.1 -exec gzip -9 {} \;

# BUILD FILES portion of spec
echo > %{filesspec}
for D in $(find %{rpmjhome} -type d | sed "s|$RPM_BUILD_ROOT||"); do
  echo "%dir %attr(755,root,root) $D"
done >> %{filesspec}
for F in $(find %{rpmjhome} -type f | sed "s|$RPM_BUILD_ROOT||"); do
  mode=$(stat -c %a $RPM_BUILD_ROOT/$F)
  echo "%attr($mode,root,root) $F"
done >> %{filesspec}
find %{rpmjhome} -type l | sed "s|$RPM_BUILD_ROOT||" >> %{filesspec}

# BUILD update-alternatives script
echo "update-alternatives \\" > %{postsh}
echo "--install %{_bindir}/java java %{javabin}/java %{priority} \\" >> %{postsh}
for F in $(find %{rpmjhome}/bin -type f | sed "s|$RPM_BUILD_ROOT||"); do
  bn=$(basename $F)
  echo "--slave %{_bindir}/$bn $bn %{javabin}/$bn \\" >> %{postsh}
done
for F in $(find %{rpmjhome}/man/man1 -type f | sed "s|$RPM_BUILD_ROOT||"); do
  bn=$(basename $F)
  echo "--slave %{_mandir}/man1/$bn $bn %{javaman}/$bn \\" >> %{postsh}
done
echo "" >> %{postsh}
cat %{postsh}

%files -f %{filesspec}

%post -f %{postsh} 

%postun
update-alternatives --remove java %{javabin}/java
