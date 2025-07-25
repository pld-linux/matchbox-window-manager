#
# Conditional build:
%bcond_without	gconf		# gconf support
%bcond_without	session		# session manager support
%bcond_without	sn		# startup-notification support
%bcond_without	composite	# composite support (experimental)
#
Summary:	Matchbox Window Manager
Summary(pl.UTF-8):	Zarządca okien dla środowiska Matchbox
Name:		matchbox-window-manager
Version:	1.2
Release:	4
License:	GPL v2+
Group:		X11/Window Managers
Source0:	http://downloads.yoctoproject.org/releases/matchbox/matchbox-window-manager/1.2/%{name}-%{version}.tar.bz2
# Source0-md5:	3e158dcf57823b55c926d95b245500fb
Patch0:		%{name}-link.patch
URL:		https://www.yoctoproject.org/software-item/matchbox/
%{?with_gconf:BuildRequires:	GConf2-devel >= 2.0}
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libmatchbox-devel >= 1.5
BuildRequires:	libtool
BuildRequires:	pkgconfig
%{?with_sn:BuildRequires:	startup-notification-devel}
%{?with_session:BuildRequires:	xorg-lib-libSM-devel}
%{?with_composite:BuildRequires:	xorg-lib-libXcomposite-devel}
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXfixes-devel >= 4.0
Requires:	libmatchbox >= 1.5
Requires:	xorg-lib-libXfixes >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Matchbox Window Manager.

%description -l pl.UTF-8
Zarządca okien dla środowiska Matchbox.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_composite:--enable-composite} \
	%{?with_gconf:--enable-gconf} \
	%{?with_session:--enable-session} \
	%{?with_sn:--enable-startup-notification}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONFTOOL=true

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with gconf}
%post
%gconf_schema_install matchbox.schemas

%preun
%gconf_schema_uninstall matchbox.schemas
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/matchbox-remote
%attr(755,root,root) %{_bindir}/matchbox-window-manager
%{_datadir}/matchbox/mbnoapp.xpm
%{_datadir}/themes/Default/matchbox
%dir %{_datadir}/themes/MBOpus
%{_datadir}/themes/MBOpus/matchbox
%dir %{_datadir}/themes/blondie
%{_datadir}/themes/blondie/matchbox
%dir %{_sysconfdir}/matchbox
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/matchbox/kbdconfig
%if %{with gconf}
%{_sysconfdir}/gconf/schemas/matchbox.schemas
%endif
