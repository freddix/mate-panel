Summary:	MATE panel
Name:		mate-panel
Version:	1.6.2
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	bffcebcc8edc10308799b3d339b67a53
URL:		http://wiki.mate-desktop.org/mate-panel
BuildRequires:	NetworkManager-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dconf-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libmateweather-devel
BuildRequires:	libmatewnck-devel
BuildRequires:	libtool
BuildRequires:	mate-desktop-devel
BuildRequires:	mate-doc-utils
BuildRequires:	mate-menus-devel
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	python-libxml2
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	rarian
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libmateweather-data
Requires:	mate-polkit
Requires:	xdg-icon-theme
Requires:	xdg-menus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
The mate-panel packages provides the MATE panel, menus and some
basic applets for the panel.

%package devel
Summary:	MATE panel includes, and more
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Panel header files for creating MATE panels.

%package libs
Summary:	MATE panel library
Group:		X11/Libraries

%description libs
MATE panel library.

%package apidocs
Summary:	panel-applet API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
panel-applet API documentation.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__gnome_doc_prepare}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_datadir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,ha,ig,la,ps}

%find_lang %{name} --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README ChangeLog
%attr(755,root,root) %{_bindir}/mate-*
%attr(755,root,root) %{_libexecdir}/clock-applet
%attr(755,root,root) %{_libexecdir}/fish-applet
%attr(755,root,root) %{_libexecdir}/notification-area-applet
%attr(755,root,root) %{_libexecdir}/wnck-applet
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/dbus-1/services/org.mate.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.WnckletFactory.service

%{_datadir}/mate-panel
%{_desktopdir}/*.desktop
%{_iconsdir}/*/*/apps/*.*
%{_mandir}/man1/*.1*

%files libs
%defattr(644,root,root,755)
%dir %{_libexecdir}
%attr(755,root,root) %ghost %{_libdir}/libmate-panel-applet-4.so.?
%attr(755,root,root) %{_libdir}/libmate-panel-applet-4.so.*.*.*
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-panel-applet-4.so
%{_includedir}/mate-panel-4.0
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/MatePanelApplet-4.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-panel-applet

