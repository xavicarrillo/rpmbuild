%define dist ito
%define disttag ito

Summary: Live Syncing (Mirror) Daemon
Name: lsyncd
Version: 2.0.7
Release: 0%{?dist}
Vendor: ITO
License: GPLv2+
Group: System Environment/Daemons
URL: http://code.google.com/p/lsyncd/
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.init
Source2: %{name}.conf
BuildRequires: autoconf automake libtool
Requires: bash >= 2.0
Requires(post): /sbin/chkconfig coreutils
Requires(preun): /sbin/chkconfig /sbin/service
Provides: lsycnd
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Lsyncd watches a local directory trees event monitor interface (inotify or fsevents). It aggregates and combines events for a few seconds and then spawns one (or more) process(es) to synchronize the changes. By default this is rsync. Lsyncd is thus a light-weight live mirror solution that is comparatively easy to install not requiring new filesystems or blockdevices and does not hamper local filesystem performance.

%prep
%setup -q

%build
%configure 
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/%{name}
install -p -m 766 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
    service %{name} stop >/dev/null 2>&1 ||:
fi

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_defaultdocdir}/%name/
%{_initrddir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_sysconfdir}/%{name}.conf

%changelog
* Thu Jul 09 2012 xcarrillo@riplife.es 2.0.7-0-ito
- Version 2.0.7

