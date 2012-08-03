%define dist nsa
%define disttag nsa
%define sbindir /sbin
%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress
 
Summary: OCS Inventory UNIX Server
Name: OCSNG_UNIX_SERVER
Version: 2.0.1
Release: 1
Vendor: nsa
License: GPLv2+
Group: System Environment/Daemons
URL: http://launchpad.net/ocsinventory-server/stable-2.0/
Source0: %{name}-%{version}.tar.gz

# Disable nsa,third-party repos first
Requires: perl >= 5.6
Requires: mysql-server >= 4.1
Requires: MySQL-client
Requires: httpd php-ldap php-mysql php-gd
Requires: mod_perl >= 1.29
Requires: mod_php >= 4.3.2
# Needs EPEL repo enabled
Requires: perl-XML-Simple perl-Compress-Raw-Zlib perl-DBI perl-DBD-MySQL perl-Apache-DBI perl-Net-IP perl-XML-Entities perl-SOAP-Lite perl-Apache2-SOAP

Requires(post): /sbin/chkconfig coreutils
Requires(preun): /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service
Provides: OCSinventory-Server
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
 
%description
Powerful inventory and package deployment system for Windows and UNIX like computers
 
%prep

%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}/%{_datadir}
mkdir -p  %{buildroot}/%{_sysconfdir}/httpd/conf.d

echo y | sh setup.sh
mv /usr/share/ocsinventory-reports/  %{buildroot}/%{_datadir}/
mv %{_sysconfdir}/httpd/conf.d/*ocsinventory* %{buildroot}/%{_sysconfdir}/httpd/conf.d/

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --levels 235 mysql on
/sbin/chkconfig --levels 235 httpd on

%postun
/sbin/service mysql restart
/sbin/service httpd restart

 
%files
%defattr(-,root,root,-)
%{_datadir}/*
%dir /var/lib/ocsinventory-reports/*
/etc/httpd/conf.d/z-ocsinventory-server.conf
/etc/httpd/conf.d/ocsinventory-reports.conf

%changelog
* Wed Sep 16 2011 xcarrillo@riplife.es 2.0.1-1nsa
- Version 2.0.1-1nsa (http://www.ocsinventory-ng.org/en/home/news/version-2-0-1-stable.html)
