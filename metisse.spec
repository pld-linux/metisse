Summary:	A 3D X Desktop
Summary(pl):	Trójwymiarowe biurko
Name:		metisse
Version:	0.3.4
Release:	1
License:	GPL
Group:		X11/Window Managers
Source0:	http://insitu.lri.fr/~chapuis/software/metisse/%{name}-%{version}.tar.bz2
# Source0-md5:	a2a3ef747da4fca36c027e0bbd858673
Source1:	%{name}.desktop
Source2:	%{name}-xsession.desktop
Patch0:		%{name}-locale_names.patch
Patch1:		%{name}-startXwnc.patch
Patch2:		%{name}-vfmg.patch
URL:		http://insitu.lri.fr/~chapuis/metisse/
BuildRequires:	XFree86-OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fribidi-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libstroke-devel
BuildRequires:	nucleo-devel >= 0.1-0.20041130.1
BuildRequires:	readline-devel
BuildRequires:	rplay-devel
Requires:	vfmg >= 0.9.18-10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_wmpropsdir	/usr/share/wm-properties

%description
Metisse is an experimental X desktop with some OpenGL capacity. It
consists of a virtual X server called Xwnc, a special version of FVWM,
and a FVWM module FvwmAmetista. Xwnc is a mix of Xvnc and XDarwin. It
draws nothing on your screen; everything is drawn into pixmaps.
Similarly to Xvnc, but with a different protocol, Xwnc can send these
pixmaps (and other information) to a "viewer". FvwmAmetista is such a
viewer; it uses OpenGL for rendering the X desktop into a window of a
"regular" 3D accelerated X server.

%description -l pl
Metisse to eksperymentalny X desktop z mo¿liwo¶ciami OpenGL. Sk³ada
siê z wirtualnego serwera o nazwie Xwnc, specialnej wersji FVWM oraz
modu³u FvwmAmetista do FVWM. Xwnc to po³±czenie Xvnc i XDarwin. Nie
rysuje nic na ekranie; wszystko jest rysowane do obrazów.
Podobnie do Xvnc, lecz przy u¿yciu innego protoko³u, Xwnc wysy³a te
obrazy (i inne informacje) do "przegl±darki". T± przegl±dark± jest
FvwmAmetista; u¿ywa OpenGL do wy¶wietlania biurka X w oknie "zwyk³ego"
serwera X z akceleracj± 3D.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
find -name "*sv_SE*" -exec rename sv_SE sv "{}" ";"

%build
%{__aclocal}
%{__autoconf}
%{__automake}
cd fvwm-insitu
%{__aclocal}
%{__autoconf}
%{__automake}
cd ..
%configure \
	--enable-freetype \
%ifarch %{ix86}
	--enable-glx-x86
%else
	--enable-glx
%endif
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/xsessions,%{_wmpropsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_wmpropsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/xsessions/%{name}.desktop

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%{_datadir}/%{name}
%{_datadir}/fvwm-insitu
%{_datadir}/xsessions/%{name}.desktop
%{_wmpropsdir}/%{name}.desktop
%{_mandir}/*/*
