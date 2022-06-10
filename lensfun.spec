Name:           lensfun
Version:        0.3.2
Release:        21
Summary:        Library to correct defects introduced by photographic lenses
License:        LGPLv3 and CC-BY-SA-3.0
URL:            http://lensfun.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Patch0001:      Only-require-glib-2.40-when-tests-are-build-without-.patch
Patch0002:      Only-use-proper-C-new-and-delete-syntax-for-object-c.patch
Patch0003:      Use-database-in-source-directory-while-running-tests.patch
Patch0004:      Patch-47-respect-DESTDIR-when-installing-python-stuf.patch
Patch0005:      Various-CMake-patches-from-the-mailing-list.patch
Patch0006:      Added-std-namespace-to-isnan.patch
Patch0007:      Pull-isnan-into-std-namespace-include-cmath-not-math.patch

BuildRequires:  cmake >= 2.8 doxygen gcc-c++ pkgconfig(glib-2.0) pkgconfig(libpng)
BuildRequires:  python3-docutils pkgconfig(zlib) python3 python3-devel

%description
The lensfun library provides an open source database of photographic lenses and
their characteristics.

%package        devel
Summary:        Development toolkit for lensfun
License:        LGPLv3
Requires:       %{name} = %{version}-%{release}
%description    devel
This package contains the libraries and header files needed to build an application
using lensfun.

%package        tools
Summary:        Tools for managing lensfun data
License:        LGPLv3
Requires:       python3-lensfun = %{version}-%{release}
%description    tools
This package contains tools for getting lens database updates and managing lenses
adapter in lensfun.

%package -n     python3-lensfun
Summary:        Python3 lensfun bindings
Requires:       %{name} = %{version}-%{release}
%description -n python3-lensfun
Library to correct defects introduced by photographic lenses.

%package        help
Summary:        Documentation for lensfun

%description    help
This package provides documentation for lensfun.

%prep
%autosetup -n lensfun-0.3.2 -p1

sed -i.shbang \
  -e "s|^#!/usr/bin/env python3$|#!%{__python3}|g" \
  apps/lensfun-add-adapter \
  apps/lensfun-update-data

%build
mkdir %{_target_platform}
cd %{_target_platform}
%{cmake} .. \
  -DBUILD_DOC:BOOL=ON \
  -DBUILD_TESTS:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DCMAKE_INSTALL_DOCDIR:PATH=%{_pkgdocdir}
cd -

%make_build -C %{_target_platform}
make doc -C %{_target_platform}

%install
%make_install/fast -C %{_target_platform}

install -d %{buildroot}/var/lib/lensfun-updates

rm -fv %{buildroot}%{_bindir}/g-lensfun-update-data \
       %{buildroot}%{_mandir}/man1/g-lensfun-update-data.*

%check
cd %{_target_platform}
export CTEST_OUTPUT_ON_FAILURE=1
ctest -vv
cd -

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%doc README.md
%license docs/cc-by-sa-3.0.txt docs/lgpl-3.0.txt
%{_datadir}/lensfun/
%{_libdir}/{liblensfun.so.%{version},liblensfun.so.1*}
%dir /var/lib/lensfun-updates/

%files devel
%{_pkgdocdir}/{*.html,*.png,*.css,*.js,*.svg}
%{_includedir}/lensfun/
%{_libdir}/liblensfun.so
%{_libdir}/pkgconfig/lensfun.pc

%files -n python3-lensfun
%{python3_sitelib}/lensfun/
%{python3_sitelib}/lensfun*.egg-info

%files tools
%{_bindir}/{lensfun-add-adapter,lensfun-update-data}

%files help
%{_mandir}/man1/lensfun-add-adapter.1*
%{_mandir}/man1/lensfun-update-data.1*

%changelog
* Tue Jun 7 2022 Chenyx <chenyixiong3@huawei.com> - 0.3.2-21
- License compliance rectification

* Fri Jan 14 2022 xu_ping <xuping33@huawei.com> - 0.3.2-20
- Packaging svg files

* Tue Feb 25 2020 fengbing <fengbing7@huawei.com> - 0.3.2-19
- Package init
