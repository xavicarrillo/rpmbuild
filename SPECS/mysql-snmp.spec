Name:           mysql-snmp
Version:        1.2
Release:        2%{?dist}
Summary:        SNMP monitoring agent for MySQL

Group:          Applications/Databases
License:        GPL
URL:            http://www.masterzen.fr/software-contributions/mysql-snmp-monitor-mysql-with-snmp
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       perl(DBI), perl(DBD::mysql) >= 1.0, perl(Unix::Syslog)
#Requires:       perl(SNMP), perl(NetSNMP::OID), perl(NetSNMP::agent), perl(NetSNMP::ASN)
#Requires:       perl(NetSNMP::agent::default_store), perl(NetSNMP::default_store)
#Requires:       net-snmp >= 5.4.3
Requires:       net-snmp >= net-snmp-5.6.1.1-2ITO
Obsoletes:      mysql-agent

# So that rpmbuild doesn't include Requires automaticaly from the binaries on %files
AutoReqProv: no

%description
mysql-snmp is a small daemon that connects to a local snmpd daemon
to report statistics on a local or remote MySQL server.

%prep
%setup -q
test "$RPM_BUILD_ROOT" == "/" || rm -rf "$RPM_BUILD_ROOT"

%install
install -d ${RPM_BUILD_ROOT}%{_sbindir}
install -d ${RPM_BUILD_ROOT}%{_initrddir}
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/snmp
install -d ${RPM_BUILD_ROOT}%{_mandir}/man1
install -d ${RPM_BUILD_ROOT}%{_datadir}/snmp/mibs
install -c -m 755 mysql-snmp ${RPM_BUILD_ROOT}%{_sbindir} 
install -c -m 755 redhat/mysql-snmp.init ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
install -c -m 644 redhat/mysql-snmp.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}
install -c -m 600 my.cnf ${RPM_BUILD_ROOT}%{_sysconfdir}/snmp
install -c -m 644 mysql-snmp.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
gzip ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-snmp.1 
install -m 644 MYSQL-SERVER-MIB.txt ${RPM_BUILD_ROOT}%{_datadir}/snmp/mibs

%post
/sbin/chkconfig mysql-snmp on
mysql -e "GRANT SELECT, PROCESS, SHOW DATABASES, SUPER, REPLICATION CLIENT ON *.* TO 'monitoring'@'localhost' IDENTIFIED BY PASSWORD '*B4DEB2B5C72C47AC460AE8E11A3221FEBC789B1A' ; FLUSH PRIVILEGES;"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README opennms/*
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/snmp/my.cnf
%doc %{_mandir}/man1/*.1*
%{_initrddir}/*
%{_datadir}/snmp/mibs/*

%changelog
* Wed Mar 29 2012 Xavi Carrillo <xcarrillo@riplife.es> - 1.2.2
- Add user monitoring, password=op3ns3sam3 
- Add Requires net-snmp >= net-snmp-5.6.1.1-2ITO

* Wed Mar 28 2012 Xavi Carrillo <xcarrillo@riplife.es> - 1.2.1
- SPT-74159
- Custom /etc/snmp/my.cnf (no user/password since it is from localhost):
	[client]
	host=localhost
	port=3306
	#user=monitoring
	#password=op3ns3sam3
- Commented out "Requires: perl(NetSNMP::OID)" so that net-snmp-perl doesn't conflict with our custom net-snmp rpm
- Add "AutoReqProv: no" so that rpmbuild doesn't include Requires automaticaly from the binaries on %files
- Enable automatic startup on the default runlevel

* Wed Feb 17 2011 Brice Figureau <brice+debian@daysofwonder.com> - 1.2
v1.2 release
* Wed Feb 17 2010 Robin Bowes <rpmbuild@yo61.net> - 1.0
v1.0 release
* Mon Nov 16 2009 Robin Bowes <rpmbuild@yo61.net> - 1.0rc2-1
Bump to rc2 version
* Sat Oct 31 2009 Brice Figureau <brice@daysofwonder.com> - 1.0rc1-1
New version
* Sat Oct 24 2009 Brice Figureau <brice@daysofwonder.com> - 0.8-1
New version
Manpage compression in the spec
* Mon Sep 28 2009 Robin Bowes <rpmbuild@yo61.net> - 0.7-2
Add opennms config files to package
* Mon Sep 28 2009 Robin Bowes <rpmbuild@yo61.net> - 0.7-1
Initial RPM packaging
