%define dist nsa
%define disttag nsa
%define sbindir /sbin
%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress
 
Summary: OCS Inventory UNIX Agent
Name: Ocsinventory-Unix-Agent
Version: 2.0.4
Release: 2
Vendor: nsa
License: GPLv2+
Group: Applications/System
URL: http://launchpad.net/ocsinventory-unix-agent/
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.cron
Source2: %{name}.conf
Source3: %{name}.update-adm.pl
BuildRequires: make
Requires: perl >= 5.8
Requires: dmidecode pciutils perl-XML-Simple perl-Net-IP
Provides: Ocsinventory-Unix-Agent
Obsoletes: ocsinventory-agent
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
 
%description
Powerful inventory and package deployment system for Windows and UNIX like computers
 
%prep

%setup -q

%build
PERL_AUTOINSTALL=1 perl Makefile.PL
make

%install
# We'll answer 'no' to the Interactive Installation question
echo n | make DESTDIR=%{buildroot} install
%{__mkdir_p} %{buildroot}/etc/cron.daily
%{__mkdir_p} %{buildroot}/etc/ocsinventory
%{__install} -p -m 755 %{SOURCE1} %{buildroot}/etc/cron.daily/ocsinventory-agent
%{__install} -p -m 600 %{SOURCE2} %{buildroot}/etc/ocsinventory/ocsinventory-agent.cfg
%{__install} -p -m 755 %{SOURCE3} %{buildroot}/usr/bin/update-adm.pl

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_usr}
%{_sysconfdir}/cron.daily
%{_sysconfdir}/ocsinventory

%post
# Get the TAG from the host name and run the client twice, so that it sends the extra stuff from update-adm.pl
sed -i s/"tag=MDEV"/tag=`hostname | awk -F. {'print $2'} | tr -s [:lower:] [:upper:]`/ /etc/ocsinventory/ocsinventory-agent.cfg
/usr/bin/ocsinventory-agent --force
perl /usr/bin/update-adm.pl
/usr/bin/ocsinventory-agent --force


%changelog
* Thu Mar 23 2012 xcarrillo@riplife.es 2.0.4-2nsa
- Add automatic TAG assignation on ocsinventory-agent.cfg (via `hostname`), so that non-puppetized hosts don't need any arrangements.
- Execute an ocs run so that the machine is inventoried right away

* Thu Mar 01 2012 xcarrillo@riplife.es 2.0.4-1nsa
- Upgrade to 2.0.4
- Fix the daily cronjob file

* Thu Dec 15 2011 xcarrillo@riplife.es 2.0.3-1nsa
- Upgrade to 2.0.3
- Works  on RHEL 4.4

* Mon Sep 30 2011 xcarrillo@riplife.es 2.0.1-2nsa
- Minor changes to update-adm.pl

* Mon Sep 21 2011 xcarrillo@riplife.es 2.0.1-1nsa
- Version 2.0.1
- Add Pablo's /usr/bin/update-adm.pl
- Add /etc/ocsinventory/ocsinventory-agent.cfg

* Mon Jul 11 2011 xcarrillo@riplife.es 2.0-1nsa
- Version 2.0

* Wed Apr 27 2011 xcarrillo@riplife.es 2.0rc2-0nsa
- Version 2.0rc2
