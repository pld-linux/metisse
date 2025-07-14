%define pre rc4
Summary:	A 3D X Desktop
Summary(pl.UTF-8):	Trójwymiarowe biurko
Name:		metisse
Version:	0.4.0
Release:	0.%{pre}.1
License:	GPL
Group:		X11/Window Managers
Source0:	http://insitu.lri.fr/metisse/download/latest/metisse-0.4.0-%{pre}.tar.bz2
# Source0-md5:	f2f5ee1b12b2ec8cae33abec132d7616
Source1:	%{name}.desktop
Source2:	%{name}-xsession.desktop
Patch0:		%{name}-locale_names.patch
Patch1:		%{name}-startXwnc.patch
Patch2:		%{name}-vfmg.patch
URL:		http://insitu.lri.fr/~chapuis/metisse/
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fribidi-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libstroke-devel
BuildRequires:	nucleo-devel >= 0.6
BuildRequires:	readline-devel
BuildRequires:	rplay-devel
Requires:	ImageMagick-coder-jpeg
Requires:	ImageMagick-coder-png
Requires:	Xwnc = %{version}-%{release}
Requires:	nucleo >= 0.6
Requires:	vfmg >= 0.9.95
Conflicts:	filesystem < 3.0-20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_wmpropsdir	/usr/share/gnome/wm-properties

%description
Metisse is an experimental X desktop with some OpenGL capacity. It
consists of a virtual X server called Xwnc, a special version of FVWM,
and a FVWM module FvwmAmetista. Xwnc is a mix of Xvnc and XDarwin. It
draws nothing on your screen; everything is drawn into pixmaps.
Similarly to Xvnc, but with a different protocol, Xwnc can send these
pixmaps (and other information) to a "viewer". FvwmAmetista is such a
viewer; it uses OpenGL for rendering the X desktop into a window of a
"regular" 3D accelerated X server.

%description -l pl.UTF-8
Metisse to eksperymentalny X desktop z możliwościami OpenGL. Składa
się z wirtualnego serwera o nazwie Xwnc, specialnej wersji FVWM oraz
modułu FvwmAmetista do FVWM. Xwnc to połączenie Xvnc i XDarwin. Nie
rysuje nic na ekranie; wszystko jest rysowane do obrazów.
Podobnie do Xvnc, lecz przy użyciu innego protokołu, Xwnc wysyła te
obrazy (i inne informacje) do "przeglądarki". Tą przeglądarką jest
FvwmAmetista; używa OpenGL do wyświetlania biurka X w oknie "zwykłego"
serwera X z akceleracją 3D.

%package -n Xwnc
Summary:	Internal metisse X server
Summary(pl.UTF-8):	Wewnętrzny serwer X metisse
Group:		X11/Applications/Networking
Conflicts:	metisse < 0.3.5-2

%description -n Xwnc
Xwnc is a mix of Xvnc and XDarwin. It draws nothing on your screen;
everything is drawn into pixmaps. Similarly to Xvnc, but with a
different protocol.

%description -n Xwnc -l pl.UTF-8
Xwnc to połączenie Xvnc i XDarwin. Nie rysuje nic na ekranie; wszystko
jest rysowane do obrazów. Podobnie do Xvnc, lecz przy użyciu innego
protokołu.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
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
%attr(755,root,root) %{_bindir}/[!X]*
%attr(755,root,root) %{_libdir}/*
%{_datadir}/%{name}
%{_datadir}/fvwm-insitu
%{_datadir}/xsessions/%{name}.desktop
%{_wmpropsdir}/%{name}.desktop
%{_mandir}/*/*

%files -n Xwnc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Xwnc
