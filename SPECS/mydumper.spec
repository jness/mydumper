Name:		mydumper	
Version:	0.2.3
Release:	1%{?dist}
Summary:	Mydumper is a high-performance multi-threaded backup toolset for MySQL and Drizzle

Group:		Applications/Databases	
License:	GPLv3	
URL:		http://www.mydumper.org/	
Source0:	http://launchpad.net/mydumper/0.2/0.2.3/+download/%{name}-%{version}.tar.gz	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	glib2-devel, zlib-devel, pcre-devel, mysql-devel, cmake	
Requires:	mysql

%description
Mydumper (aka. MySQL Data Dumper) is a high-performance multi-threaded backup 
(and restore) toolset for MySQL and Drizzle.  The main developers originally worked
as Support Engineers at MySQL (one has moved to Facebook and another to SkySQL) 
and this is how they would envisage mysqldump based on years of user feedback.


%prep
%setup -q -n %{name}-%{version}


%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/mydumper
%{_bindir}/myloader


%changelog
* Fri Jul 15 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.2.3-1
- initial build
