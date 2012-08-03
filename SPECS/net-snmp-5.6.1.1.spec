%define dist ito
%define disttag ito
%define	sbindir	/sbin

Summary: Simple Network Management Protocol (SNMP)
Name: net-snmp
Version: 5.6.1.1
Release: 2%{?dist}
Vendor: ito
License: GPLv2+
Group: System Environment/Daemons
URL: http://www.net-snmp.org/
Source0: %{name}-%{version}.tar.gz
Source1: snmpd.conf
Source2: snmpd.init
Source3: sitescope
#Source4: snmpd_cpu.sh
#Source5: disk_space.sh
BuildRequires: zlib-devel
BuildRequires: autoconf automake libtool
Requires: bash >= 2.0
Requires(post): /sbin/chkconfig coreutils
Requires(preun): /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service
Provides: net-snmp
Conflicts: net-snmp-libs
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Simple Network Management Protocol (SNMP) is a widely used protocol for monitoring the health and welfare of network equipment (eg. routers), computer equipment and even devices like UPSs. Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6. 

%prep
%setup -q
%build
%configure --without-openssl \
           --without-rpm \
           --disable-des \
           --disable-privacy \
           --disable-ipv6 \
           --with-default-snmp-version=3 \
           --with-persistent-directory=/var/net-snmp \
           --with-logfile=/var/log/snmpd.log \
           --disable-embedded-perl \
           --disable-perl-cc-checks \
           --with-mib-modules=ucd-snmp/pass \
           --with-mib-modules=ucd-snmp/extensible \
           --with-out-mib-modules=snmpv3mibs \
           --with-sys-contact="snmp@kazootek.com" \
           --with-sys-location="Canada"
make
umask 022

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=%{buildroot} install

mkdir -p $RPM_BUILD_ROOT/etc/snmp
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/usr/local/admin
install -p -m 744 %{SOURCE1} $RPM_BUILD_ROOT/etc/snmp/
install -p -m 655 %{SOURCE2} $RPM_BUILD_ROOT/etc/init.d/snmpd
cp -a %{SOURCE3} $RPM_BUILD_ROOT/usr/local/admin/

#install -p -m 655 %{SOURCE4} $RPM_BUILD_ROOT/usr/local/admin
#install -p -m 655 %{SOURCE5} $RPM_BUILD_ROOT/usr/local/admin
#install -p -m 644 %{_sourcedir}/%{name}-files/%{version}/snmpd.conf %{buildroot}/etc/snmp/
#install -p -m 755 %{_sourcedir}/%{name}-files/%{version}/snmpd.init %{buildroot}/etc/init.d/snmpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add snmpd
#/sbin/service snmpd restart

%preun
if [ $1 = 0 ]; then
    service snmpd stop >/dev/null 2>&1 ||:
    /sbin/chkconfig --del rsyslog
fi

%postun
if [ "$1" -ge "1" ]; then
    service snmpd condrestart > /dev/null 2>&1 ||:
fi	

%files
%defattr(-,root,root,-)
%{_datadir}/snmp

%{_bindir}
%{_sbindir}
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/*.so*
%{_includedir}
%{_libdir}/*.a
%{_libdir}/*.la

/usr/lib64/perl5/5.8.8/x86_64-linux-thread-multi/perllocal.pod
/usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/SNMP.pm
/usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/Bundle/Makefile.subs.pl
/usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/Bundle/NetSNMP/.packlist
#%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/*
#%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/NetSNMP/ASN/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/NetSNMP/OID/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/NetSNMP/TrapReceiver/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/NetSNMP/agent/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/NetSNMP/agent/default_store/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/NetSNMP/default_store/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/auto/SNMP/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/NetSNMP/*
%dir /usr/lib64/perl5/site_perl/5.8.8/x86_64-linux-thread-multi/NetSNMP/agent/*
%dir /usr/local/admin/sitescope/*
/etc/init.d/snmpd
/etc/snmp/snmpd.conf

%changelog
* Tue Mar 29 2012 xcarrillo@riplife.es 5.6.1.1-2ito
- Add messy sitescope scripts and configs so that alarms don't break up when updating net-snmp
* Tue Mar 27 2012 xcarrillo@riplife.es 5.6.1.1-1ito
- Version 5.6.1.1
* Thu Apr 20 2011 xcarrillo@riplife.es 5.6.1-0nsa
- Version 5.6.1

