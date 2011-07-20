Name:           mydumper
Version:        0.2.3
Release:        4%{?dist}
Summary:        A high-performance multi-threaded backup toolset for MySQL and Drizzle

Group:          Applications/Databases
License:        GPLv3
URL:            http://www.mydumper.org/
Source0:        http://launchpad.net/mydumper/0.2/0.2.3/+download/%{name}-%{version}.tar.gz

# man pages built from fedora 14
# due to low version of python-docutil.
# docutils 0.6 is required by Sphinx to
# create the man pages.
Source1:        mydumper.1.gz
Source2:        myloader.1.gz

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Patch0:         mydumper_cmake_suffix.patch
Patch1:         mydumper_cmake_sphinx.patch

BuildRequires:  glib2-devel, zlib-devel, pcre-devel, mysql-devel, cmake

%if 0%{?rhel} > 6
BuildRequires:  python-sphinx10, python-docutils
%endif

%if 0%{?fedora} > 12
BuildRequires:  python-sphinx, python-docutils
%endif

%description
Mydumper (aka. MySQL Data Dumper) is a high-performance multi-threaded 
backup (and restore) toolset for MySQL and Drizzle.  The main developers 
originally worked as Support Engineers at MySQL (one has moved to 
Facebook and another to SkySQL) and this is how they would envisage mysqldump 
based on years of user feedback.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

# on el6 we use python-sphinx10 from EPEL
# so we need to patch the cmake Sphinx locator
%if 0%{?rhel} > 6
%patch1 -p1
%endif

%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if 0%{?rhel} == 5
# install our man pages
%{__install} -p -d -m 0755 %{buildroot}%{_mandir}/man1/
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/mydumper
%{_bindir}/myloader
%{_mandir}/man1/mydumper.1.gz
%{_mandir}/man1/myloader.1.gz

# docs only exist if created via sphinx
# this is el6 and fedora
%if (0%{?rhel} > 6 || 0%{?fedora} > 12)
%doc %{_docdir}/mydumper/
%endif


%changelog
* Wed Jul 20 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.2.3-4
- Docs and man pages built on el6 and fedora

* Tue Jul 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.2.3-3
- adding man pages manually due to low level python-docutil
  in epel5

* Fri Jul 15 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.2.3-2
- removing CMakeLists.txt from doc
- removing Requires: mysql

* Fri Jul 15 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.2.3-1
- initial build
